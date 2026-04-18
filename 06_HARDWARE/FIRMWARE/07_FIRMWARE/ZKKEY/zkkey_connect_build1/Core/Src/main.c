/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : ZKKey Build 1 — ATECC608 Wake + I2C Scan
  *                   DEBUG: I2C running at 10kHz (extra slow for wake timing)
  *                   If this works, we tune back up to 100kHz.
  ******************************************************************************
  */
/* USER CODE END Header */

#include "main.h"

/* USER CODE BEGIN Includes */
#include <stdio.h>
#include <string.h>
/* USER CODE END Includes */

/* USER CODE BEGIN PTD */
/* USER CODE END PTD */

/* USER CODE BEGIN PD */
#define ATECC_I2C_ADDR     0x60
#define SCAN_INTERVAL_MS   5000
/* USER CODE END PD */

/* USER CODE BEGIN PM */
/* USER CODE END PM */

I2C_HandleTypeDef hi2c1;
UART_HandleTypeDef huart2;

/* USER CODE BEGIN PV */
char uart_buf[128];
/* USER CODE END PV */

void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_I2C1_Init(void);
static void MX_USART2_UART_Init(void);

/* USER CODE BEGIN PFP */
void uart_print(const char *str);
void atecc_wake(void);
void i2c_scan(void);
/* USER CODE END PFP */

/* USER CODE BEGIN 0 */

void uart_print(const char *str)
{
    HAL_UART_Transmit(&huart2, (uint8_t*)str, strlen(str), 200);
}

/*
 * Wake sequence — method 2 only (zero byte to address 0x00).
 * At 10kHz this gives the ATECC plenty of time to see the transition
 * and complete its internal wake sequence before we probe it.
 * NACK is expected — the chip is waking, not ACKing.
 */
void atecc_wake(void)
{
    uint8_t zero = 0x00;
    HAL_I2C_Master_Transmit(&hi2c1, 0x00, &zero, 1, 10);

    /*
     * tWHI = Wake High to Data Communications delay.
     * Datasheet min = 1.5ms. At 10kHz we give it 10ms to be safe.
     * If 10kHz works we can reduce this after tuning.
     */
    HAL_Delay(10);
}

void i2c_scan(void)
{
    uint8_t found = 0;

    uart_print("\r\n========================================\r\n");
    uart_print("  ZKKey I2C Scan — 10kHz Debug Mode\r\n");
    uart_print("========================================\r\n");

    /* Re-init I2C to clear any stuck state from previous scan */
    uart_print("  Re-initializing I2C1 at 10kHz...\r\n");
    HAL_I2C_DeInit(&hi2c1);
    HAL_Delay(10);
    MX_I2C1_Init();
    HAL_Delay(10);
    uart_print("  I2C1 ready at 10kHz.\r\n");

    /* Wake the ATECC */
    uart_print("  Sending wake sequence...\r\n");
    atecc_wake();
    uart_print("  Wake sent. Waiting 10ms...\r\n");
    HAL_Delay(10);

    /* Scan all addresses */
    uart_print("  Scanning 0x01 to 0x7F...\r\n");
    uart_print("----------------------------------------\r\n");

    for (uint16_t addr = 1; addr < 128; addr++)
    {
        /*
         * 3 retries, 50ms timeout per attempt.
         * Extra generous timeout at 10kHz — each bit takes 100us,
         * so a full 9-bit address takes ~900us. 50ms is way more
         * than enough even if the chip is slow to respond.
         */
        HAL_StatusTypeDef result = HAL_I2C_IsDeviceReady(
            &hi2c1, (uint16_t)(addr << 1), 3, 50);

        if (result == HAL_OK)
        {
            sprintf(uart_buf, "  *** ACK at 0x%02X", (uint8_t)addr);
            uart_print(uart_buf);

            if (addr == ATECC_I2C_ADDR)
                uart_print(" <-- ATECC608! SUCCESS!\r\n");
            else
                uart_print(" <-- unknown device\r\n");

            found++;
        }
    }

    uart_print("----------------------------------------\r\n");

    if (found == 0)
    {
        uart_print("  NO DEVICES FOUND.\r\n");

        uint32_t err = HAL_I2C_GetError(&hi2c1);
        sprintf(uart_buf, "  I2C error register: 0x%08lX\r\n", err);
        uart_print(uart_buf);

        if (err & 0x00000001) uart_print("  -> BUS ERROR\r\n");
        if (err & 0x00000002) uart_print("  -> ARBITRATION LOST\r\n");
        if (err & 0x00000008) uart_print("  -> OVERRUN\r\n");
        if (err & 0x00000020) uart_print("  -> TIMEOUT — SDA/SCL stuck low\r\n");
        if (err == 0x00000004 || err == 0x00000000)
            uart_print("  -> Clean bus. Device not responding to address.\r\n");
    }
    else
    {
        sprintf(uart_buf, "  Found %d device(s). Done.\r\n", (int)found);
        uart_print(uart_buf);
    }

    uart_print("========================================\r\n");
    sprintf(uart_buf, "  Next scan in %d seconds...\r\n",
            SCAN_INTERVAL_MS / 1000);
    uart_print(uart_buf);
}

/* USER CODE END 0 */

int main(void)
{
    HAL_Init();
    SystemClock_Config();
    MX_GPIO_Init();
    MX_I2C1_Init();
    MX_USART2_UART_Init();

    /* USER CODE BEGIN 2 */
    uart_print("\r\n\r\n");
    uart_print("************************************\r\n");
    uart_print("  ZKNOT ZKKey Connect — Build 1\r\n");
    uart_print("  10kHz I2C Debug Build\r\n");
    uart_print("  If ATECC responds here we tune up\r\n");
    uart_print("************************************\r\n");
    uart_print("  SDA = PB7 = SDA/D14 on CN10\r\n");
    uart_print("  SCL = PB6 = SCL/D15 on CN10\r\n");
    uart_print("  I2C speed: 10kHz\r\n");
    uart_print("  Target: ATECC608 @ 0x60\r\n");
    uart_print("************************************\r\n");
    /* USER CODE END 2 */

    /* USER CODE BEGIN WHILE */
    while (1)
    {
        /* USER CODE END WHILE */

        /* USER CODE BEGIN 3 */
        i2c_scan();
        HAL_Delay(SCAN_INTERVAL_MS);
    }
    /* USER CODE END 3 */
}

void SystemClock_Config(void)
{
    RCC_OscInitTypeDef RCC_OscInitStruct = {0};
    RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

    if (HAL_PWREx_ControlVoltageScaling(PWR_REGULATOR_VOLTAGE_SCALE1) != HAL_OK)
        Error_Handler();

    RCC_OscInitStruct.OscillatorType      = RCC_OSCILLATORTYPE_HSI;
    RCC_OscInitStruct.HSIState            = RCC_HSI_ON;
    RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
    RCC_OscInitStruct.PLL.PLLState        = RCC_PLL_ON;
    RCC_OscInitStruct.PLL.PLLSource       = RCC_PLLSOURCE_HSI;
    RCC_OscInitStruct.PLL.PLLM            = 1;
    RCC_OscInitStruct.PLL.PLLN            = 10;
    RCC_OscInitStruct.PLL.PLLP            = RCC_PLLP_DIV7;
    RCC_OscInitStruct.PLL.PLLQ            = RCC_PLLQ_DIV2;
    RCC_OscInitStruct.PLL.PLLR            = RCC_PLLR_DIV2;
    if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
        Error_Handler();

    RCC_ClkInitStruct.ClockType      = RCC_CLOCKTYPE_HCLK | RCC_CLOCKTYPE_SYSCLK
                                     | RCC_CLOCKTYPE_PCLK1 | RCC_CLOCKTYPE_PCLK2;
    RCC_ClkInitStruct.SYSCLKSource   = RCC_SYSCLKSOURCE_PLLCLK;
    RCC_ClkInitStruct.AHBCLKDivider  = RCC_SYSCLK_DIV1;
    RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;
    RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

    if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_4) != HAL_OK)
        Error_Handler();
}

/*
 * I2C1 at 10kHz — deliberately slow for wake sequence debugging.
 *
 * LEARNING NOTE — I2C Timing register:
 * The STM32L4 I2C uses a single 32-bit TIMINGR register instead of
 * separate SCL high/low time registers like older STM32s.
 * The value is calculated by ST's CubeMX or timing calculator tool.
 *
 * 0x10D19CE4 = 100kHz @ 80MHz PCLK (standard)
 * 0x707CB81B = 10kHz  @ 80MHz PCLK (debug — 10x slower)
 *
 * At 10kHz each bit takes 100 microseconds instead of 10.
 * This gives the ATECC608 maximum time to respond to each clock edge.
 */
static void MX_I2C1_Init(void)
{
    hi2c1.Instance              = I2C1;
    hi2c1.Init.Timing           = 0x707CB81B;   /* 10kHz @ 80MHz — DEBUG SLOW */
    hi2c1.Init.OwnAddress1      = 0;
    hi2c1.Init.AddressingMode   = I2C_ADDRESSINGMODE_7BIT;
    hi2c1.Init.DualAddressMode  = I2C_DUALADDRESS_DISABLE;
    hi2c1.Init.OwnAddress2      = 0;
    hi2c1.Init.OwnAddress2Masks = I2C_OA2_NOMASK;
    hi2c1.Init.GeneralCallMode  = I2C_GENERALCALL_DISABLE;
    hi2c1.Init.NoStretchMode    = I2C_NOSTRETCH_DISABLE;

    if (HAL_I2C_Init(&hi2c1) != HAL_OK)
        Error_Handler();

    if (HAL_I2CEx_ConfigAnalogFilter(&hi2c1, I2C_ANALOGFILTER_ENABLE) != HAL_OK)
        Error_Handler();

    if (HAL_I2CEx_ConfigDigitalFilter(&hi2c1, 0) != HAL_OK)
        Error_Handler();
}

static void MX_USART2_UART_Init(void)
{
    huart2.Instance                    = USART2;
    huart2.Init.BaudRate               = 115200;
    huart2.Init.WordLength             = UART_WORDLENGTH_8B;
    huart2.Init.StopBits               = UART_STOPBITS_1;
    huart2.Init.Parity                 = UART_PARITY_NONE;
    huart2.Init.Mode                   = UART_MODE_TX_RX;
    huart2.Init.HwFlowCtl              = UART_HWCONTROL_NONE;
    huart2.Init.OverSampling           = UART_OVERSAMPLING_16;
    huart2.Init.OneBitSampling         = UART_ONE_BIT_SAMPLE_DISABLE;
    huart2.AdvancedInit.AdvFeatureInit = UART_ADVFEATURE_NO_INIT;

    if (HAL_UART_Init(&huart2) != HAL_OK)
        Error_Handler();
}

static void MX_GPIO_Init(void)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};

    __HAL_RCC_GPIOC_CLK_ENABLE();
    __HAL_RCC_GPIOH_CLK_ENABLE();
    __HAL_RCC_GPIOA_CLK_ENABLE();
    __HAL_RCC_GPIOB_CLK_ENABLE();

    HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_RESET);

    GPIO_InitStruct.Pin  = GPIO_PIN_13;
    GPIO_InitStruct.Mode = GPIO_MODE_IT_FALLING;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);

    GPIO_InitStruct.Pin   = GPIO_PIN_5;
    GPIO_InitStruct.Mode  = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull  = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
}

void Error_Handler(void)
{
    __disable_irq();
    while (1) {}
}

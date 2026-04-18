/*
 * ZKAuth Module Firmware
 * For Seeed XIAO RP2040
 * 
 * This firmware handles:
 * - ATECC608B secure element communication
 * - Physical authentication button
 * - Status LED control
 * - I2C command interface with keyboard
 * 
 * Author: Corne ZKAuth Project
 * Date: February 13, 2026
 * Version: 1.0
 */

#include <Wire.h>
#include <cryptoauthlib.h>

// Pin Definitions
#define BTN_PIN         D0    // Authentication button
#define LED_GREEN_PIN   D1    // Ready LED
#define LED_RED_PIN     D2    // Busy LED
#define I2C_SDA         D7    // I2C Data
#define I2C_SCL         D8    // I2C Clock

// I2C Addresses
#define ATECC608_ADDR   0x60  // ATECC608B address
#define MODULE_ADDR     0x50  // This module's I2C address (for keyboard communication)

// Command codes
#define CMD_AUTH        0x01  // Request authentication
#define CMD_STATUS      0x02  // Get status
#define CMD_GET_PUBKEY  0x03  // Get public key

// Status codes
#define STATUS_IDLE     0x00
#define STATUS_READY    0x01
#define STATUS_BUSY     0x02
#define STATUS_SUCCESS  0x03
#define STATUS_ERROR    0xFF

// ATECC608B configuration
ATCAIfaceCfg cfg_atecc608_i2c = {
    .iface_type             = ATCA_I2C_IFACE,
    .devtype                = ATECC608,
    .atcai2c.slave_address  = 0x60,
    .atcai2c.bus            = 1,
    .atcai2c.baud           = 400000,
    .wake_delay             = 1500,
    .rx_retries             = 20,
    .cfg_data               = &Wire
};

// Global variables
uint8_t currentStatus = STATUS_IDLE;
uint8_t signature[64];      // ECDSA signature buffer
uint8_t challenge[32];      // Challenge from keyboard
bool buttonPressed = false;
unsigned long buttonPressTime = 0;
const unsigned long AUTH_TIMEOUT = 30000; // 30 second timeout

void setup() {
  // Initialize serial for debugging
  Serial.begin(115200);
  while (!Serial && millis() < 3000); // Wait up to 3s for serial
  
  Serial.println("ZKAuth Module v1.0");
  Serial.println("Initializing...");
  
  // Initialize pins
  pinMode(BTN_PIN, INPUT_PULLUP);
  pinMode(LED_GREEN_PIN, OUTPUT);
  pinMode(LED_RED_PIN, OUTPUT);
  
  // Initial LED state (both off)
  digitalWrite(LED_GREEN_PIN, LOW);
  digitalWrite(LED_RED_PIN, LOW);
  
  // Initialize I2C as slave
  Wire.setSDA(I2C_SDA);
  Wire.setSCL(I2C_SCL);
  Wire.begin(MODULE_ADDR);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);
  
  // Initialize ATECC608B
  ATCA_STATUS status = atcab_init(&cfg_atecc608_i2c);
  if (status != ATCA_SUCCESS) {
    Serial.print("ATECC608B init failed: ");
    Serial.println(status, HEX);
    blinkError();
  } else {
    Serial.println("ATECC608B initialized successfully");
    
    // Read device serial number
    uint8_t serialNum[9];
    status = atcab_read_serial_number(serialNum);
    if (status == ATCA_SUCCESS) {
      Serial.print("Device Serial: ");
      for (int i = 0; i < 9; i++) {
        if (serialNum[i] < 0x10) Serial.print("0");
        Serial.print(serialNum[i], HEX);
      }
      Serial.println();
    }
  }
  
  // Set status to idle
  currentStatus = STATUS_IDLE;
  digitalWrite(LED_GREEN_PIN, HIGH); // Green = ready
  
  Serial.println("Initialization complete. Ready for commands.");
}

void loop() {
  // Check authentication button
  checkButton();
  
  // Handle authentication timeout
  if (currentStatus == STATUS_READY) {
    if (millis() - buttonPressTime > AUTH_TIMEOUT) {
      Serial.println("Authentication timeout");
      currentStatus = STATUS_IDLE;
      digitalWrite(LED_GREEN_PIN, HIGH);
      digitalWrite(LED_RED_PIN, LOW);
    }
  }
  
  delay(10); // Small delay to prevent excessive polling
}

// I2C receive event (command from keyboard)
void receiveEvent(int numBytes) {
  if (numBytes == 0) return;
  
  uint8_t cmd = Wire.read();
  
  switch (cmd) {
    case CMD_AUTH:
      handleAuthRequest();
      break;
      
    case CMD_STATUS:
      // Status will be sent on next request
      break;
      
    case CMD_GET_PUBKEY:
      handlePubKeyRequest();
      break;
      
    default:
      Serial.print("Unknown command: ");
      Serial.println(cmd, HEX);
      break;
  }
}

// I2C request event (keyboard requesting data)
void requestEvent() {
  // Send current status
  Wire.write(currentStatus);
  
  // If authentication successful, send signature
  if (currentStatus == STATUS_SUCCESS) {
    Wire.write(signature, 64);
    currentStatus = STATUS_IDLE;
    digitalWrite(LED_GREEN_PIN, HIGH);
    digitalWrite(LED_RED_PIN, LOW);
  }
}

// Handle authentication request from keyboard
void handleAuthRequest() {
  Serial.println("Authentication request received");
  
  // Read challenge from keyboard (32 bytes)
  if (Wire.available() >= 32) {
    Wire.readBytes(challenge, 32);
    
    Serial.print("Challenge: ");
    for (int i = 0; i < 32; i++) {
      if (challenge[i] < 0x10) Serial.print("0");
      Serial.print(challenge[i], HEX);
    }
    Serial.println();
    
    // Set status to ready (waiting for button press)
    currentStatus = STATUS_READY;
    buttonPressTime = millis();
    
    // Blink green LED to indicate ready
    digitalWrite(LED_GREEN_PIN, HIGH);
    digitalWrite(LED_RED_PIN, LOW);
    
    Serial.println("Waiting for button press...");
  } else {
    Serial.println("Error: Insufficient data for challenge");
    currentStatus = STATUS_ERROR;
  }
}

// Handle public key request
void handlePubKeyRequest() {
  Serial.println("Public key request received");
  
  uint8_t pubkey[64];
  ATCA_STATUS status = atcab_get_pubkey(0, pubkey);
  
  if (status == ATCA_SUCCESS) {
    Serial.print("Public key: ");
    for (int i = 0; i < 64; i++) {
      if (pubkey[i] < 0x10) Serial.print("0");
      Serial.print(pubkey[i], HEX);
    }
    Serial.println();
    
    // Public key will be sent on next I2C request
    currentStatus = STATUS_SUCCESS;
    memcpy(signature, pubkey, 64); // Reuse signature buffer
  } else {
    Serial.print("Error reading public key: ");
    Serial.println(status, HEX);
    currentStatus = STATUS_ERROR;
  }
}

// Check authentication button state
void checkButton() {
  static bool lastButtonState = HIGH;
  bool buttonState = digitalRead(BTN_PIN);
  
  // Detect button press (falling edge)
  if (lastButtonState == HIGH && buttonState == LOW) {
    delay(50); // Debounce
    buttonState = digitalRead(BTN_PIN);
    
    if (buttonState == LOW && !buttonPressed) {
      buttonPressed = true;
      onButtonPress();
    }
  }
  
  // Detect button release
  if (lastButtonState == LOW && buttonState == HIGH) {
    delay(50); // Debounce
    buttonPressed = false;
  }
  
  lastButtonState = buttonState;
}

// Handle button press event
void onButtonPress() {
  Serial.println("Button pressed!");
  
  // Only perform authentication if in READY state
  if (currentStatus == STATUS_READY) {
    performAuthentication();
  } else {
    Serial.println("Not in ready state - ignoring button press");
  }
}

// Perform ECDSA signature with ATECC608B
void performAuthentication() {
  Serial.println("Performing authentication...");
  
  // Set status to busy
  currentStatus = STATUS_BUSY;
  
  // Turn on red LED (busy)
  digitalWrite(LED_GREEN_PIN, LOW);
  digitalWrite(LED_RED_PIN, HIGH);
  
  // Sign the challenge using ATECC608B
  // Slot 0 contains the private key
  ATCA_STATUS status = atcab_sign(0, challenge, signature);
  
  if (status == ATCA_SUCCESS) {
    Serial.println("Signature generated successfully!");
    Serial.print("Signature: ");
    for (int i = 0; i < 64; i++) {
      if (signature[i] < 0x10) Serial.print("0");
      Serial.print(signature[i], HEX);
    }
    Serial.println();
    
    // Set status to success
    currentStatus = STATUS_SUCCESS;
    
    // Blink green LED (success)
    for (int i = 0; i < 3; i++) {
      digitalWrite(LED_GREEN_PIN, HIGH);
      digitalWrite(LED_RED_PIN, LOW);
      delay(100);
      digitalWrite(LED_GREEN_PIN, LOW);
      digitalWrite(LED_RED_PIN, HIGH);
      delay(100);
    }
    
    digitalWrite(LED_GREEN_PIN, HIGH);
    digitalWrite(LED_RED_PIN, LOW);
    
  } else {
    Serial.print("Signature generation failed: ");
    Serial.println(status, HEX);
    
    // Set status to error
    currentStatus = STATUS_ERROR;
    blinkError();
  }
}

// Blink red LED to indicate error
void blinkError() {
  for (int i = 0; i < 5; i++) {
    digitalWrite(LED_RED_PIN, HIGH);
    delay(200);
    digitalWrite(LED_RED_PIN, LOW);
    delay(200);
  }
  digitalWrite(LED_GREEN_PIN, HIGH); // Return to ready
}

/*
 * ATECC608B Key Provisioning
 * 
 * This function should be run ONCE during initial setup to generate
 * and lock the private key in the ATECC608B.
 * 
 * WARNING: This is a ONE-TIME operation! Once locked, keys cannot be changed!
 */
void provisionDevice() {
  Serial.println("=== DEVICE PROVISIONING ===");
  Serial.println("WARNING: This will permanently lock the device!");
  Serial.println("Press button within 10 seconds to continue...");
  
  unsigned long startTime = millis();
  while (millis() - startTime < 10000) {
    if (digitalRead(BTN_PIN) == LOW) {
      delay(50); // Debounce
      if (digitalRead(BTN_PIN) == LOW) {
        break;
      }
    }
  }
  
  if (millis() - startTime >= 10000) {
    Serial.println("Provisioning cancelled");
    return;
  }
  
  Serial.println("Starting provisioning...");
  
  // Generate new private key in slot 0
  uint8_t pubkey[64];
  ATCA_STATUS status = atcab_genkey(0, pubkey);
  
  if (status != ATCA_SUCCESS) {
    Serial.print("Key generation failed: ");
    Serial.println(status, HEX);
    return;
  }
  
  Serial.println("Private key generated successfully!");
  Serial.print("Public key (X): ");
  for (int i = 0; i < 32; i++) {
    if (pubkey[i] < 0x10) Serial.print("0");
    Serial.print(pubkey[i], HEX);
  }
  Serial.println();
  Serial.print("Public key (Y): ");
  for (int i = 32; i < 64; i++) {
    if (pubkey[i] < 0x10) Serial.print("0");
    Serial.print(pubkey[i], HEX);
  }
  Serial.println();
  
  // Lock data zone (makes private key permanent)
  Serial.println("Locking data zone...");
  status = atcab_lock_data_zone();
  
  if (status != ATCA_SUCCESS) {
    Serial.print("Lock failed: ");
    Serial.println(status, HEX);
    return;
  }
  
  Serial.println("=== PROVISIONING COMPLETE ===");
  Serial.println("Device is now locked and ready for use!");
  
  // Celebrate with LED pattern
  for (int i = 0; i < 10; i++) {
    digitalWrite(LED_GREEN_PIN, HIGH);
    delay(100);
    digitalWrite(LED_GREEN_PIN, LOW);
    digitalWrite(LED_RED_PIN, HIGH);
    delay(100);
    digitalWrite(LED_RED_PIN, LOW);
  }
  digitalWrite(LED_GREEN_PIN, HIGH);
}

/* 
 * To enable provisioning mode:
 * Uncomment the following line in setup()
 * Upload once, then comment it back out for normal operation
 */
// provisionDevice();

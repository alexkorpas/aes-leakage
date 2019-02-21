// #include <compiler.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// AES block size in bytes
#define AES_BLOCK_SIZE 16

// Total number of rounds for AES-128
#define AES_NUM_OF_ROUNDS 10

// Key schedule size
#define AES_KEY_SCHEDULE_SIZE ((AES_BLOCK_SIZE) * (AES_NUM_OF_ROUNDS + 1))
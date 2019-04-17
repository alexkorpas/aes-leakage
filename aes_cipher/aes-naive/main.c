#include <stdio.h>
// #include "conf_example.h"
// #include "crypt.h"
#include "aes.h"


/** Global Variable declaration **/

/* Key Initialization vector */
uint8_t key_vectors[]
	= {0x54, 0x68, 0x61, 0x74, 0x73, 0x20, 0x6D, 0x79, 0x20, 0x4B, 0x75, 0x6E, 0x67, 0x20, 0x46, 0x75};
    // = {0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f};
    // = {0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c};

/*  Initialization vector
 * Note: AES Standard FIPS SP800-38A provides detailed explanation
 * on generation of init_vector for different CFB modes
 */
// #if (AES_CBC == true) | (AES_CFB == true) | (AES_OFB == true)

// uint8_t init_vector[]
//     = {0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f};

// #endif

/* Input plain text data that are to be encrypted */
// uint8_t pText[] = {"Input_Text_blck1Input_Text_blck2Input_Text_blck3Input_Text_blck4"};
/* array to store the encrypted message */
// uint8_t cText[128];
/* array to store the decrypted message */
// uint8_t pText1[128];

/*!
 * \brief Main application function.                              \n
 * -> Initialize USART0 for print functions                       \n
 * -> Initialize AES to generate Key schedule for AES-128         \n
 * -> Based on the AES mode enabled in conf_example.h file,       \n
 *    execute encryption and decryption of a message and          \n
 *    compare them against input data to check its functionality. \n
 * -> The decrypted message can be viewed on the COM port terminal \n
 */
int main(void)
{
	uint8_t full_key[AES_KEY_SCHEDULE_SIZE];
	uint8_t i;
	/* Generate key schedule for AES-128 from the Cipher Key */
	aes_init(key_vectors, full_key);

	/* Print status messages */
	printf("AES key generated successfully!..\r\n");

	for (i = 0; i < AES_NUM_OF_ROUNDS; i ++) {
		printf("Round Key %d: %02X %02X %02X %02X %02X %02X %02X %02X %02X %02X %02X %02X %02X %02X %02X %02X\n", i, 
			full_key[16 * i + 0 ], full_key[16 * i + 1 ], full_key[16 * i + 2 ], full_key[16 * i + 3 ],
			full_key[16 * i + 4 ], full_key[16 * i + 5 ], full_key[16 * i + 6 ], full_key[16 * i + 7 ],
			full_key[16 * i + 8 ], full_key[16 * i + 9 ], full_key[16 * i + 10], full_key[16 * i + 11],
			full_key[16 * i + 12], full_key[16 * i + 13], full_key[16 * i + 14], full_key[16 * i + 15]);
	}

	/* Print Input message for user */
	// printf("\n The message to be encrypted is:\r\n");
	// printf("\n %s \r\n", pText);
}

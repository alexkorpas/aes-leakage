/**
 * \file AES-128 five confidentiality modes demo example using
 *        Software Library
 *
 * Copyright (c) 2015 Atmel Corporation. All rights reserved.
 *
 * \asf_license_start
 *
 * \page License
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice,
 *    this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 *    this list of conditions and the following disclaimer in the documentation
 *    and/or other materials provided with the distribution.
 *
 * 3. The name of Atmel may not be used to endorse or promote products derived
 *    from this software without specific prior written permission.
 *
 * 4. This software may only be redistributed and used in connection with an
 *    Atmel microcontroller product.
 *
 * THIS SOFTWARE IS PROVIDED BY ATMEL "AS IS" AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT ARE
 * EXPRESSLY AND SPECIFICALLY DISCLAIMED. IN NO EVENT SHALL ATMEL BE LIABLE FOR
 * ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
 * STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
 * ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 *
 * \asf_license_stop
 *
 */
/**
 * Support and FAQ: visit <a href="http://www.atmel.com/design-support/">Atmel Support</a>
 */

#include <atmel_start.h>
#include <stdio.h>
#include "usart_io.h"
#include "conf_example.h"
#include "crypt.h"

#if defined(__GNUC__)
static FILE mystdout = FDEV_SETUP_STREAM(usart0_putchar, NULL, _FDEV_SETUP_WRITE);
#endif

/** Global Variable declaration **/

/* Key Initialization vector */
uint8_t key_vectors[]
    = {0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c};

/*  Initialization vector
 * Note: AES Standard FIPS SP800-38A provides detailed explanation
 * on generation of init_vector for different CFB modes
 */
#if (AES_CBC == true) | (AES_CFB == true) | (AES_OFB == true)

uint8_t init_vector[]
    = {0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f};

#endif

/* Input plain text data that are to be encrypted */
uint8_t pText[] = {"Input_Text_blck1Input_Text_blck2Input_Text_blck3Input_Text_blck4"};
/* array to store the encrypted message */
uint8_t cText[64];
/* array to store the decrypted message */
uint8_t pText1[64];

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
	/* Initializes MCU, drivers and middleware */
	atmel_start_init();
#if defined(__GNUC__)
	stdout = &mystdout;
#endif

	/* Generate key schedule for AES-128 from the Cipher Key */
	aes_init(key_vectors);

	/* Print status messages */
	printf("AES key generated successfully!..\r\n");

	/* Print Input message for user */
	printf("\n The message to be encrypted is:\r\n");
	printf("\n %s \r\n", pText);

/*
 * Perform ECB, CFB, OFB, CTR and CBC Encryption and Decryption
 * based on the mode enabled in conf_example.h. User can choose
 * the mode that he wants to evaluate. By default, all modes are
 * enabled.
 * The decrypted message is printed to USART0.
 * If the decrypted message is same as the input plain text,
 * it ensures the working of each mode.
 */
#if (AES_ECB == true)

	// Perform ECB Encryption
	ecb_encrypt(pText, cText, sizeof(pText));
	for (volatile int i = 0; i < 1000; i++)
		;
	// Perform ECB Decryption
	ecb_decrypt(cText, pText1, sizeof(cText));
	// Print decrypted message
	printf("\n Decrypted message using AES-ECB mode : \r\n");
	printf("\n %s \r\n", pText1);

#endif

#if (AES_CFB == true)

	// Perform CFB Encryption
	cfb_encrypt(pText, cText, init_vector, CFB_MODE_128, sizeof(pText));
	for (volatile int i = 0; i < 1000; i++)
		;
	// Perform CFB Decryption
	cfb_decrypt(cText, pText1, init_vector, CFB_MODE_128, sizeof(cText));
	// Print decrypted message
	printf("\n Decrypted message using AES-CFB mode : \r\n");
	printf("\n %s \r\n", pText1);

#endif

#if (AES_OFB == true)

	// Perform OFB Encryption
	ofb_encrypt(pText, cText, init_vector, sizeof(pText));
	for (volatile int i = 0; i < 1000; i++)
		;
	// Perform OFB Decryption
	ofb_encrypt(cText, pText1, init_vector, sizeof(cText));
	// Print decrypted message
	printf("\n Decrypted message using AES-OFB mode : \r\n");
	printf("\n %s \r\n", pText1);

#endif

#if (AES_CTR == true)

	/* Initialize Counter block with initialization vector,
	 * nonce and counter value
	 */
	ctr_blk_t counter_vector = {.i_vector = AES_CTR_IVECTOR, .nonce = AES_CTR_NONCE, .counter = AES_CTR_COUNTER};
	// Perform CTR Encryption
	ctr_encrypt_decrypt(pText, cText, &counter_vector, sizeof(pText));
	// Send Counter block value to decryptor
	for (volatile int i = 0; i < 1000; i++)
		;
	counter_vector.i_vector = AES_CTR_IVECTOR;
	counter_vector.nonce    = AES_CTR_NONCE;
	counter_vector.counter  = AES_CTR_COUNTER;
	// Perform CTR Decryption
	ctr_encrypt_decrypt(cText, pText1, &counter_vector, sizeof(pText1));
	// Print decrypted message
	printf("\n Decrypted message using AES-CTR mode : \r\n");
	printf("\n %s \r\n", pText1);

#endif

/*! \warning CBC mode is done at the last as it process input plain text
 * during encryption and so the plain text value is not retained.
 * For testing purpose, to preserve the input plan text for testing with
 * other modes, this mode is added at the last.
 */
#if (AES_CBC == true)

	// Perform CBC Encryption
	cbc_encrypt(pText, cText, init_vector, sizeof(pText));
	for (volatile int i = 0; i < 1000; i++)
		;
	// Perform CBC Decryption
	cbc_decrypt(cText, pText1, init_vector, sizeof(cText));
	// Print decrypted message
	printf("\n Decrypted message using AES-CBC mode : \r\n");
	printf("\n %s \r\n", pText1);

#endif

	/* Forever loop */
	while (1)
		;
}

//////////////////////////////////////////////////////////////////////////////
// * File name: main.c
// *                                                                          
// * Description:  Main function.
// * Note:  Currently Host PC connection is very unstable.
//          Migration to other DSP platform is necessary
// * Author: Jihoon Lee
// *                                                                          
//////////////////////////////////////////////////////////////////////////////

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include "ezdsp5502.h"
#include "Dsplib.h"
#include "fft.h"
#include <string.h>

#define IMAGESIZE 128
#define ENC_KEY 0.93
#define DEC_KEY 0.21

#pragma DATA_SECTION(IMAGE_R, "sdram_0")
#pragma DATA_SECTION(IMAGE_G, "sdram_0")
#pragma DATA_SECTION(IMAGE_B, "sdram_0")
#pragma DATA_SECTION(IMAGE_R_ANS, "sdram_0")
#pragma DATA_SECTION(IMAGE_G_ANS, "sdram_0")
#pragma DATA_SECTION(IMAGE_B_ANS, "sdram_0")
#pragma DATA_SECTION(key_gen, "sdram_0")
float IMAGE_R[IMAGESIZE][2*IMAGESIZE+1];
float IMAGE_G[IMAGESIZE][2*IMAGESIZE+1];
float IMAGE_B[IMAGESIZE][2*IMAGESIZE+1];
float IMAGE_R_ANS[IMAGESIZE][2*IMAGESIZE+1];
float IMAGE_G_ANS[IMAGESIZE][2*IMAGESIZE+1];
float IMAGE_B_ANS[IMAGESIZE][2*IMAGESIZE+1];
float key_gen[2*IMAGESIZE+1];

void Forward_FFT()
{
    int row = 0;
    for (row = 0; row < IMAGESIZE; row++)
    {
        four1(IMAGE_R[row],IMAGESIZE,1);
        four1(IMAGE_G[row],IMAGESIZE,1);
        four1(IMAGE_B[row],IMAGESIZE,1);
    }
}

void Reverse_FFT()
{
    int row = 0;
    for (row = 0; row < IMAGESIZE; row++)
    {
        four1(IMAGE_R[row],IMAGESIZE,-1);
        four1(IMAGE_G[row],IMAGESIZE,-1);
        four1(IMAGE_B[row],IMAGESIZE,-1);
    }
}

void FFT_Mask_On()
{
    // Masking Process for FFT coefficients
    //
    int row, column;
    for (row = 0; row < IMAGESIZE; row++)
    {
        for (column = 0; column < IMAGESIZE; column++)
        {
            IMAGE_R[row][2*column+1] *= key_gen[2*column+1];
            IMAGE_R[row][2*column+2] *= key_gen[2*column+2];
            IMAGE_G[row][2*column+1] *= key_gen[2*column+1];
            IMAGE_G[row][2*column+2] *= key_gen[2*column+2];
            IMAGE_B[row][2*column+1] *= key_gen[2*column+1];
            IMAGE_B[row][2*column+2] *= key_gen[2*column+2];
        }
    }
}

void FFT_Mask_Off()
{
    // Unmasking Process for FFT coefficients
    //
    int row, column;
    for (row = 0; row < IMAGESIZE; row++)
    {
        for (column = 0; column < IMAGESIZE; column++)
        {
            IMAGE_R[row][2*column+1] /= key_gen[2*column+1];
            IMAGE_R[row][2*column+2] /= key_gen[2*column+2];
            IMAGE_G[row][2*column+1] /= key_gen[2*column+1];
            IMAGE_G[row][2*column+2] /= key_gen[2*column+2];
            IMAGE_B[row][2*column+1] /= key_gen[2*column+1];
            IMAGE_B[row][2*column+2] /= key_gen[2*column+2];
        }
    }
}

void main( void )
{
    int row, column, i;
    //FILE *fp;               // Source Image: Currently Host PC files cannot be loaded due to hardware problems
    //FILE *fp2;              // Output Image: Currently Host PC files cannot be loaded due to hardware problems

    /* Initialization of Logistic Map on FFT coefficeint Mask */
    key_gen[0] = ENC_KEY;
    for (row = 0; row <= 2*IMAGESIZE; row++)
    {
        if (row == 0)
            key_gen[row] = ENC_KEY;
        else
            key_gen[row] = 3.828 * key_gen[row-1] * (1 - key_gen[row-1]);
        printf("%f\n", key_gen[row]);
    }


    EZDSP5502_init( );



    //fp = fopen("C://Users//jihoon//Desktop//DSP_ENC//lena_128.ppm", "r");

    for (row = 0; row < IMAGESIZE; row++)
    {
        for (column = 0; column < IMAGESIZE; column++)
        {
            float red,green,blue;
            red = (float)(255 - 2 *column);
            green = (float)(column+128);
            blue = (float)(column);
            //c = fgetc(fp);
            IMAGE_R[row][2*column+1] = red;
            IMAGE_R[row][2*column+2] = 0.0;
            IMAGE_R_ANS[row][2*column+1] = red;
            IMAGE_R_ANS[row][2*column+2] = 0.0;
            //c = fgetc(fp);
            IMAGE_G[row][2*column+1] = green;
            IMAGE_G[row][2*column+2] = 0.0;
            IMAGE_G_ANS[row][2*column+1] = green;
            IMAGE_G[row][2*column+2] = 0.0;
            //c = fgetc(fp);
            IMAGE_B[row][2*column+1] = blue;
            IMAGE_B[row][2*column+2] = 0.0;
            IMAGE_B_ANS[row][2*column+1] = blue;
            IMAGE_B_ANS[row][2*column+2] = 0.0;
            //IMAGE[row][column][rgb] = c ^ (c >> 1);
            //printf("Row %d Column %d = %f %f %f \n", row,column,IMAGE_R[row][2*column+1], IMAGE_G[row][2*column+1], IMAGE_B[row][2*column+1] );
        }
        //if ((row % 10) == 0)
           // printf("%d\n",row);

    }
    //fp2 = fopen("C://Users//jihoon//Desktop//DSP_ENC//output.bin", "w");

    // Encryption
    Forward_FFT();
    FFT_Mask_On();

    // If DEC_KEY does not match ENC_KEY, picture will not be recovered correctly.
    key_gen[0] = DEC_KEY;
    for (row = 0; row <= 2*IMAGESIZE; row++)
    {
        if (row == 0)
            key_gen[row] = ENC_KEY;
        else
            key_gen[row] = 3.828 * key_gen[row-1] * (1 - key_gen[row-1]);
        printf("%f\n", key_gen[row]);
    }

    // Decryption
    FFT_Mask_Off();
    Reverse_FFT();

    for (row = 0; row < IMAGESIZE; row++)
    {
        for (column = 0; column < IMAGESIZE; column++)
        {

            if ((unsigned char)IMAGE_R_ANS[row][column] != (unsigned char)(IMAGE_R[row][column] / 128.0)   )
                printf("Error at Row %d, Column %d, RED  %f %f \n",row,column, IMAGE_R_ANS[row][column], IMAGE_R[row][column]/128.0);
            if ((unsigned char)IMAGE_G_ANS[row][column] != (unsigned char)(IMAGE_G[row][column] / 128.0)   )
                printf("Error at Row %d, Column %d, GREEN  %f %f\n",row,column, IMAGE_G_ANS[row][column], IMAGE_G[row][column]/128.0);
            if ((unsigned char)IMAGE_B_ANS[row][column] != (unsigned char)(IMAGE_B[row][column] / 128.0)   )
                printf("Error at Row %d, Column %d, BLUE  %f %f\n",row,column, IMAGE_B_ANS[row][column], IMAGE_B[row][column]/128.0);
        }
    }


   /*
    * Legacy code for binary file writing.
    * Due to unstable connection with host PC, writing file is not a good way to check data validity.
    *

   for (row = 0; row < IMAGESIZE; row++)
   {
      for (column = 0; column < IMAGESIZE; column++)
      {
          //printf("%f ", (IMAGE_R[row][2*column+1]));
          //printf("%f \n", (IMAGE_R[row][2*column+1]/128.0) );
          //printf("%x \n", (unsigned char) (IMAGE_R[row][2*column+1]/128.0) );
          //printf("Row %d Column %d = %f %f %f \n", row,column,IMAGE_R[row][2*column+1], IMAGE_G[row][2*column+1], IMAGE_B[row][2*column+1] );
          fprintf(fp2,"%c", (unsigned char) (IMAGE_R[row][2*column+1]/128.0) );
          fprintf(fp2,"%c", (unsigned char) (IMAGE_G[row][2*column+1]/128.0) );
          fprintf(fp2,"%c", (unsigned char) (IMAGE_B[row][2*column+1]/128.0) );
      }
   }

   fclose(fp);
   fclose(fp2);
   */
}



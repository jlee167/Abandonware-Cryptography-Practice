package jihoonlee.myapplication;

import android.graphics.Bitmap;
import android.graphics.drawable.BitmapDrawable;
import android.media.Image;

import java.nio.charset.StandardCharsets;
import java.security.InvalidKeyException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.ShortBufferException;
import javax.crypto.spec.SecretKeySpec;

public class ImageCrypt {

    public Bitmap target_bitmap;
    public Cipher cipher;
    public byte [] CryptKey;


    public ImageCrypt() {

    }

    private void register_image(BitmapDrawable imageIn) {
        target_bitmap = imageIn.getBitmap();
        target_bitmap = target_bitmap.copy(target_bitmap.getConfig(), true);
    }

    private void initCipher(String password, String CryptType, int mode) {
        // Nested try/catch needs to be Examined
        MessageDigest password_digest;
        try {
            password_digest = MessageDigest.getInstance("SHA-256");
            password_digest.update(password.getBytes(StandardCharsets.UTF_8), 0, password.length());
            CryptKey = password_digest.digest();
            SecretKeySpec secretKeySpec = new SecretKeySpec(CryptKey, "AES");
            cipher = Cipher.getInstance(CryptType);
            cipher.init(mode, secretKeySpec);
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        } catch (InvalidKeyException e) {
            e.printStackTrace();
        } catch (NoSuchPaddingException e) {
            e.printStackTrace();
        }
    }

    public void process_image() {
        int height = target_bitmap.getHeight();
        int width = target_bitmap.getWidth();

        int [] pixels = new int[height * width];
        target_bitmap.getPixels(pixels,0,width,0,0, width,height);
        byte [] BitmapArray = new byte[4 * height * width];
        byte [] CipherArray = new byte[4 * height * width];
        System.gc();

        for (int i = 0 ; i < height; i++) {
            for (int j = 0; j < width; j++) {
                BitmapArray[4*(i*width+j)] = (byte) pixels[i*width+j];
                BitmapArray[4*(i*width+j)+1] = (byte) (pixels[i*width+j] >> 8);
                BitmapArray[4*(i*width+j)+2] = (byte) (pixels[i*width+j] >> 16);
                BitmapArray[4*(i*width+j)+3] = (byte) (pixels[i*width+j] >> 24);
            }
        }

        try {
            cipher.doFinal(BitmapArray,0,4*height*width, CipherArray);
        } catch (BadPaddingException e) {
            e.printStackTrace();
        } catch (IllegalBlockSizeException e) {
            e.printStackTrace();
        } catch (ShortBufferException e) {
            e.printStackTrace();
        }


        for (int i = 0 ; i < height; i++) {
            for (int j = 0; j < width; j++) {
                pixels[i*width + j] = (CipherArray[i*width + j] + (CipherArray[i*width + j + 1] << 8) +
                        (CipherArray[i*width + j + 2] << 16) + (CipherArray[i*width + j + 3] << 24));
            }
        }

        target_bitmap.setPixels(pixels, 0,width,0,0,width,height);
    }

}

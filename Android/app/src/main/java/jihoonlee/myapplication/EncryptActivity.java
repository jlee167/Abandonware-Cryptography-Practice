package jihoonlee.myapplication;

import android.content.Intent;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.BitmapDrawable;
import android.net.Uri;
import android.os.Message;
import android.provider.MediaStore;
import android.support.annotation.Nullable;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.TabLayout;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import java.io.FileNotFoundException;
import java.io.InputStream;
import java.nio.Buffer;
import java.nio.ByteBuffer;
import java.nio.IntBuffer;
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


public class EncryptActivity extends AppCompatActivity {

    // AppBar Instance
    private android.support.v7.widget.Toolbar appbar_launch;

    // Encryption/Decryption type
    private enum CryptType {
        AES, RSA, XORSHIFT
    }

    // Operation Flags
    private static int RESULT_IMAGE_LOAD = 1;
    private static boolean IS_IMAGE_LOADED = false;
    private static boolean IS_IMAGE_ENCRYTED = false;
    private static boolean AREA_SEL_MODE = false;

    private TabLayout cryptTypeSel;
    private byte [] CryptKey;

    // File I/O UI variables
    private Button OpenFolderBtn;
    private Button OpenFileBtn;
    private ImageView OpenFolderImg;
    private ImageView OpenFileImg;

    // Control I/O
    private Button AreaSelBtn;
    private Button StartBtn;

    // Image to encrypt
    private ImageView target_image;

    // Encryption type specification
    private CryptType encryptionType;

    private FloatingActionButton SaveBtn;

    Cipher cipher;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_encrypt);

        // Initial tab = AES
        encryptionType = CryptType.AES;

        // Nested try/catch needs to be Examined
        MessageDigest password_digest;
        try {
            String password = getIntent().getStringExtra("PASSWORD");
            password_digest = MessageDigest.getInstance("SHA-256");
            password_digest.update(password.getBytes(StandardCharsets.UTF_8), 0, password.length());
            CryptKey = password_digest.digest();
            SecretKeySpec secretKeySpec = new SecretKeySpec(CryptKey, "AES");
            cipher = Cipher.getInstance("AES/CBC/NoPadding");
            cipher.init(Cipher.ENCRYPT_MODE, secretKeySpec);
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        } catch (InvalidKeyException e) {
            e.printStackTrace();
        } catch (NoSuchPaddingException e) {
            e.printStackTrace();
        }

        // Disable ImageView until it is loaded with an image
        target_image = findViewById(R.id.pic_encrypt);
        target_image.setVisibility(View.GONE);

        // Initilize Filo I/O UI
        OpenFolderBtn = findViewById(R.id.OpenFolderBtn);
        OpenFileBtn = findViewById(R.id.OpenFileBtn);
        OpenFolderImg = findViewById(R.id.OpenFolderImg);
        OpenFileImg = findViewById(R.id.OpenFileImg);

        OpenFileBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent photoPickerIntent = new Intent(Intent.ACTION_PICK);
                photoPickerIntent.setType("image/*");
                startActivityForResult(photoPickerIntent, RESULT_IMAGE_LOAD);
            }
        });

        // Operation Buttons
        // Selection Operation area, Starting encryption
        AreaSelBtn = findViewById(R.id.AreaBtn);
        StartBtn = findViewById(R.id.StartBtn);

        AreaSelBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                AREA_SEL_MODE = !AREA_SEL_MODE;
                if (AREA_SEL_MODE)
                    AreaSelBtn.setText("Finish");
                else
                    AreaSelBtn.setText("Select Area");
            }
        });

        StartBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (!IS_IMAGE_LOADED)
                    return;
                else {
                    Bitmap ImageBitmap = ((BitmapDrawable)target_image.getDrawable()).getBitmap();
                    ImageBitmap = ImageBitmap.copy(ImageBitmap.getConfig(), true);

                    int height = ImageBitmap.getHeight();
                    int width = ImageBitmap.getWidth();

                    int [] pixels = new int[height * width];
                    ImageBitmap.getPixels(pixels,0,width,0,0, width,height);
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

                    ImageBitmap.setPixels(pixels, 0,width,0,0,width,height);
                    target_image.setImageBitmap(ImageBitmap);

                }
            }
        });

        appbar_launch = findViewById(R.id.toolbar_Encrypt);
        appbar_launch.setTitle("Encryption");
        setSupportActionBar(appbar_launch);

        cryptTypeSel = findViewById(R.id.TypeTab);
        cryptTypeSel.addOnTabSelectedListener(new TabLayout.OnTabSelectedListener() {
            @Override
            public void onTabSelected(TabLayout.Tab tab) {
                int position = tab.getPosition();
                if (position == 0)
                    encryptionType = CryptType.AES;
                else if (position == 1)
                    encryptionType = CryptType.RSA;
                else if (position == 2)
                    encryptionType = CryptType.XORSHIFT;
            }

            @Override
            public void onTabUnselected(TabLayout.Tab tab) {
            }

            @Override
            public void onTabReselected(TabLayout.Tab tab) {
            }
        });
    }

    @Override
    protected void onStart() {
        super.onStart();
    }

    @Override
    protected void onResume() {
        super.onResume();
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == RESULT_IMAGE_LOAD && resultCode == RESULT_OK && null != data) {
            if (resultCode == RESULT_OK) {
                try {
                    final Uri imageUri = data.getData();
                    final InputStream imageStream = getContentResolver().openInputStream(imageUri);
                    final Bitmap selectedImage = BitmapFactory.decodeStream(imageStream);
                    target_image.setImageBitmap(selectedImage);
                    setImageVisible();
                    IS_IMAGE_LOADED = true;
                } catch (FileNotFoundException e) {
                    e.printStackTrace();
                    //Toast.makeText(PostImage.this, "Something went wrong", Toast.LENGTH_LONG).show();
                }

            }else {
                //Toast.makeText(PostImage.this, "You haven't picked Image",Toast.LENGTH_LONG).show();
            }
        }
    }

    private void setImageVisible() {
        OpenFolderBtn.setVisibility(View.GONE);
        OpenFileBtn.setVisibility(View.GONE);
        OpenFolderImg.setVisibility(View.GONE);
        OpenFileImg.setVisibility(View.GONE);
        target_image.setVisibility(View.VISIBLE);
    }

}

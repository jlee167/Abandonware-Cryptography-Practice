package jihoonlee.myapplication;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import com.beardedhen.androidbootstrap.BootstrapButton;
import android.widget.Button;
import android.widget.EditText;

public class PasswordActivity extends AppCompatActivity {

    private BootstrapButton ConfirmBtn;
    private EditText Password;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_password);


        ConfirmBtn = findViewById(R.id.confirmbtn);
        Password = findViewById(R.id.Password);

        ConfirmBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent next_cryptActivity = new Intent(getApplicationContext(), EncryptActivity.class);
                String CryptKey = (String)Password.getText().toString();
                next_cryptActivity.putExtra("PASSWORD", CryptKey);
                startActivity(next_cryptActivity);
            }
        });

    }
}

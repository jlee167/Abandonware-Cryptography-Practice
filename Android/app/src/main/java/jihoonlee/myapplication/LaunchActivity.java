package jihoonlee.myapplication;

import android.app.Application;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.View;
import android.widget.Button;
import android.widget.Toolbar;
import com.beardedhen.androidbootstrap.TypefaceProvider;


public class LaunchActivity extends AppCompatActivity {


    private Button EncryptBtn;
    private Button DecryptBtn;
    private Button CloudBtn;
    private Intent EncryptActivity;
    private Intent DecryptActivity;
    private Intent CloudActivity;
    private Intent PasswordActivity;
    private android.support.v7.widget.Toolbar appbar_launch;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_launch);

        EncryptBtn = (Button) findViewById(R.id.EncryptBtn);
        DecryptBtn = (Button) findViewById(R.id.DecryptBtn);
        CloudBtn = (Button) findViewById(R.id.CloudBtn);
        EncryptActivity = new Intent(getApplicationContext(), jihoonlee.myapplication.EncryptActivity.class);
        DecryptActivity = new Intent(getApplicationContext(), jihoonlee.myapplication.DecryptActivity.class);
        CloudActivity = new Intent(getApplicationContext(), jihoonlee.myapplication.CloudActivity.class);
        PasswordActivity = new Intent(getApplicationContext(), jihoonlee.myapplication.PasswordActivity.class);
        appbar_launch = findViewById(R.id.toolbar_launch);
        appbar_launch.setTitle("Image cryptographer");
        setSupportActionBar(appbar_launch);


        EncryptBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(PasswordActivity);
            }
        });

        DecryptBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(PasswordActivity);
            }
        });

        CloudBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(CloudActivity);
            }
        });
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.launch_action, menu);
        return true;
    }

    @Override
    protected void onStart() {
        super.onStart();
    }

    @Override
    protected void onResume() {
        super.onResume();
    }
}

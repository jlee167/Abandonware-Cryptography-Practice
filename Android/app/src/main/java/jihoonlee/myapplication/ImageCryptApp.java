package jihoonlee.myapplication;

import android.app.Application;

import com.beardedhen.androidbootstrap.TypefaceProvider;

public class ImageCryptApp extends Application {
    @Override public void onCreate() {
        super.onCreate();
        TypefaceProvider.registerDefaultIconSets();
    }
}

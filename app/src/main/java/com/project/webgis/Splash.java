package com.project.webgis;

import android.content.BroadcastReceiver;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.project.webgis.activity.LoginActivity;
import com.project.webgis.activity.MainActivity;
import com.project.webgis.adapter.DataManager;
import com.project.webgis.adapter.NetworkReceiver;
import com.project.webgis.adapter.SessionManager;

public class Splash extends AppCompatActivity {
    DataManager dataManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_splash);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        SessionManager sessionManager = new SessionManager(getApplicationContext());
        if (sessionManager.isLoggedIn()) {
            sessionManager.logoutUser();
        }

        dataManager = new DataManager(getApplicationContext());

        if (dataManager.isDataAvailable("HOST")) {
            new Handler().postDelayed(new Runnable() {
                @Override
                public void run() {
                    startActivity(new Intent(Splash.this, MainActivity.class));
                    finish();
                }
            }, 3000);
        } else {
            popupSaveHost();
        }
    }

    private void popupSaveHost() {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("Input host");

        final EditText input = new EditText(this);
        LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.MATCH_PARENT);
        input.setLayoutParams(lp);
        builder.setView(input);

        // Set up the buttons
        builder.setPositiveButton("Save", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                dataManager.saveData("HOST", input.getText().toString());
                Toast.makeText(getApplicationContext(), "Host server berhasil disimpan!", Toast.LENGTH_LONG).show();

                startActivity(new Intent(Splash.this, MainActivity.class));
                finish();

            }
        });
        builder.setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                Toast.makeText(getApplicationContext(), "Harup masukan host server!", Toast.LENGTH_LONG).show();
                finish();
                System.exit(0);
            }
        });
        builder.show();

    }

    @Override
    protected void onStop() {
        super.onStop();
    }
}
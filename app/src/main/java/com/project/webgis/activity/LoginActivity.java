package com.project.webgis.activity;

import android.app.ProgressDialog;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.android.volley.DefaultRetryPolicy;
import com.android.volley.NetworkError;
import com.android.volley.ParseError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.ServerError;
import com.android.volley.TimeoutError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.google.android.material.textfield.TextInputEditText;
import com.project.webgis.API;
import com.project.webgis.R;
import com.project.webgis.Splash;
import com.project.webgis.adapter.DataManager;
import com.project.webgis.adapter.SessionManager;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class LoginActivity extends AppCompatActivity {

    private TextInputEditText usernameEdit, passwordEdt;
    private String username, password;
    private Button btnLogin;
    private ProgressDialog mProgress;
    private SessionManager sessionManager;
    private DataManager dataManager;
    private RequestQueue mQueue;
    private String HOST;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        mQueue = Volley.newRequestQueue(this);

        sessionManager = new SessionManager(getApplicationContext());
        dataManager = new DataManager(getApplicationContext());

        usernameEdit = findViewById(R.id.username);
        passwordEdt = findViewById(R.id.password);
        btnLogin = findViewById(R.id.login);
        mProgress = new ProgressDialog(this);

        HOST = dataManager.getData("HOST");

        btnLogin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                loginUser();
            }
        });
    }

    private void loginUser() {
        mProgress.setCancelable(false);
        mProgress.setMessage("Signing in...");
        mProgress.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        mProgress.show();

        username = usernameEdit.getText().toString();
        password = passwordEdt.getText().toString();

        String url = HOST + API.LOGIN_URL + "?username=" + username + "&password=" + password;

        JsonObjectRequest request = new JsonObjectRequest(Request.Method.GET, url, null,
                response -> {
                    try {
                        String status = response.getString("status");
                        String message = response.getString("message");
                        if (status.equals("200")) {
                            Toast.makeText(this, "Welcome : '" + username +"'", Toast.LENGTH_LONG).show();
                            sessionManager.createLoginSession(username, username);
                            startActivity(new Intent(getApplicationContext(), MainActivity.class));
                        } else {
                            Toast.makeText(this, "Login failed: "+message, Toast.LENGTH_LONG).show();
                        }

                        mProgress.hide();

                    } catch (JSONException e) {
                        e.printStackTrace();
                        Log.i("Login Request", e.getMessage());
                        mProgress.hide();
                    }
                }, error -> {
            if (error instanceof TimeoutError) {
                Log.i("Login Request", "onErrorResponse: Timeout");
                Toast.makeText(this, "Time out", Toast.LENGTH_LONG).show();
            } else if (error instanceof ServerError) {
                Log.i("Login Request", "onErrorResponse: Server error");
                Toast.makeText(this, "Server error", Toast.LENGTH_LONG).show();
            } else if (error instanceof NetworkError) {
                Toast.makeText(this, "Network error", Toast.LENGTH_LONG).show();
            } else if (error instanceof ParseError) {
                Log.i("Login Request", "onErrorResponse: Parse error");
                Toast.makeText(this, "Parse error", Toast.LENGTH_LONG).show();
            } else {
                Log.i("Login Request", "onErrorResponse: Something went wrong ");
                Toast.makeText(this, "Other error", Toast.LENGTH_LONG).show();
            }
        });
        request.setRetryPolicy(new DefaultRetryPolicy(15000,DefaultRetryPolicy.DEFAULT_MAX_RETRIES,DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));
        request.setShouldCache(false);
        mQueue.add(request);
    }
}
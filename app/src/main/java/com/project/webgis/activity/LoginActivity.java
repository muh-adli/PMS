package com.project.webgis.activity;

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
import com.project.webgis.R;
import com.project.webgis.Splash;
import com.project.webgis.adapter.SessionManager;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class LoginActivity extends AppCompatActivity {

    private EditText usernameEdit, passwordEdt;
    private String username, password;
    private Button btnLogin;
    private ProgressBar loading;
    private SessionManager sessionManager;

    private RequestQueue mQueue;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        mQueue = Volley.newRequestQueue(this);

        sessionManager = new SessionManager(getApplicationContext());

        usernameEdit = (EditText) findViewById(R.id.username);
        passwordEdt = (EditText) findViewById(R.id.password);
        btnLogin = (Button) findViewById(R.id.login);
        loading = (ProgressBar) findViewById(R.id.loading);

        btnLogin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                loginUser();
            }
        });
    }

    private void loginUser() {
        loading.setVisibility(View.VISIBLE);
        username = usernameEdit.getText().toString();
        password = passwordEdt.getText().toString();

        String url = "https://d64e-114-5-213-161.ngrok-free.app/api/v1/account/loginRequest?username="+ username +"&password="+ password;

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

                        loading.setVisibility(View.INVISIBLE);

                    } catch (JSONException e) {
                        e.printStackTrace();
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
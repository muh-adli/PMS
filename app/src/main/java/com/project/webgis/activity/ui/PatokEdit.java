package com.project.webgis.activity.ui;

import android.content.Context;
import android.content.IntentFilter;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.android.volley.DefaultRetryPolicy;
import com.android.volley.NetworkError;
import com.android.volley.ParseError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.ServerError;
import com.android.volley.TimeoutError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.project.webgis.API;
import com.project.webgis.R;
import com.project.webgis.adapter.DataManager;

import org.json.JSONException;

public class PatokEdit extends AppCompatActivity {
    private RequestQueue mQueue;
    private DataManager dataManager;
    private String HOST;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_patok_edit);

        mQueue = Volley.newRequestQueue(this);
        dataManager = new DataManager(this);

        HOST = dataManager.getData("HOST");

        int id = getIntent().getIntExtra("id", 0);
        String afdeling = getIntent().getStringExtra("afdeling");
        String block = getIntent().getStringExtra("block");
        String nomor = getIntent().getStringExtra("nomor");
        String latitude = getIntent().getStringExtra("latitude");
        String longtitude = getIntent().getStringExtra("longtitude");
        String period = getIntent().getStringExtra("period");
        String status = getIntent().getStringExtra("status");

        EditText editAfdeling = findViewById(R.id.afdeling);
        EditText editBlock = findViewById(R.id.block);
        EditText editNomor = findViewById(R.id.noPatok);
        EditText editLatitude = findViewById(R.id.latitude);
        EditText editLongtitude = findViewById(R.id.longtitude);
        EditText editStatus = findViewById(R.id.status);
        Spinner periodSpinner = findViewById(R.id.period);
        Button updateButton = findViewById(R.id.updateButton);

        if (!isOnline()) {
            updateButton.setEnabled(false);
        }

        editAfdeling.setText(afdeling);
        editBlock.setText(block);
        editNomor.setText(nomor);
        editLatitude.setText(latitude);
        editLongtitude.setText(longtitude);
        editStatus.setText(status);

        String[] items = new String[] {"-", "Q1", "Q2", "Q3", "Q4"};
        ArrayAdapter<String> adapter = new ArrayAdapter<>(this, android.R.layout.simple_spinner_dropdown_item, items);
        periodSpinner.setAdapter(adapter);

        updateButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String selectedPeriod = periodSpinner.getSelectedItem().toString();
                updatePatok(id, selectedPeriod);
            }
        });
    }

    private void updatePatok(int id, String period) {
        String url = HOST + API.PATOK_SAVE + id + "?period=" + period;

        JsonObjectRequest request = new JsonObjectRequest(Request.Method.GET, url, null,
                response -> {
                    try {
                        String status = response.getString("status");
                        String message = response.getString("message");
                        if (status.equals("200")) {
                            Toast.makeText(this, "Patok updated", Toast.LENGTH_LONG).show();
                            finish();
                        } else {
                            Toast.makeText(this, "Update patok failed: "+message, Toast.LENGTH_LONG).show();
                            finish();
                        }

                    } catch (JSONException e) {
                        e.printStackTrace();
                        Log.i("Login Request", e.getMessage());
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

    public boolean isOnline() {
        ConnectivityManager cm = (ConnectivityManager) this.getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo netInfo = cm.getActiveNetworkInfo();
        return netInfo != null && netInfo.isConnectedOrConnecting();
    }
}
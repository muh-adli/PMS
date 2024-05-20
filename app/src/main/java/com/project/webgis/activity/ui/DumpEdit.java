package com.project.webgis.activity.ui;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.EditText;
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
import com.project.webgis.API;
import com.project.webgis.R;
import com.project.webgis.adapter.DataManager;

import org.json.JSONException;

import java.text.SimpleDateFormat;
import java.util.Calendar;

public class DumpEdit extends AppCompatActivity {
    private RequestQueue mQueue;
    private DataManager dataManager;
    private String HOST;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_dump_edit);

        mQueue = Volley.newRequestQueue(this);
        dataManager = new DataManager(this);

        HOST = dataManager.getData("HOST");

        int id = getIntent().getIntExtra("id", 0);
        String afdeling = getIntent().getStringExtra("afdeling");
        String block = getIntent().getStringExtra("block");
        String location = getIntent().getStringExtra("location");
        String dump_date = getIntent().getStringExtra("dump_date");

        EditText editAfdeling = findViewById(R.id.afdeling);
        EditText editBlock = findViewById(R.id.block);
        EditText editLocation = findViewById(R.id.location);
        DatePicker editDate = findViewById(R.id.date);
        Button updateButton = findViewById(R.id.updateButton);

        editAfdeling.setText(afdeling);
        editBlock.setText(block);
        editLocation.setText(location);

        if (!dump_date.equals("null")) {
            String mYear = dump_date.split("-")[0];
            String mMonth = dump_date.split("-")[1];
            String mDate = dump_date.split("-")[2];
            editDate.init(Integer.parseInt(mYear), Integer.parseInt(mMonth)-1, Integer.parseInt(mDate), null);
        }

        updateButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                int year = editDate.getYear();
                int month = editDate.getMonth();
                int day = editDate.getDayOfMonth();

                Calendar calendar = Calendar.getInstance();
                calendar.set(year, month, day);

                SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd");
                String strDate = format.format(calendar.getTime());

                updateTankos(id, strDate);
            }
        });
    }

    private void updateTankos(int id, String date) {
        String url = HOST + API.DUMP_SAVE + id + "?date=" + date;

        JsonObjectRequest request = new JsonObjectRequest(Request.Method.GET, url, null,
                response -> {
                    try {
                        String status = response.getString("status");
                        String message = response.getString("message");
                        if (status.equals("200")) {
                            Toast.makeText(this, "Dump updated", Toast.LENGTH_LONG).show();
                            finish();
                        } else {
                            Toast.makeText(this, "Update dump failed: "+message, Toast.LENGTH_LONG).show();
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
}
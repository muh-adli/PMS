package com.project.webgis.activity.ui.Monitor;

import android.os.Bundle;
import android.util.Log;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.TableRow;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.core.content.ContextCompat;
import androidx.fragment.app.Fragment;

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

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class ChildMonitorPatok extends Fragment {

    LinearLayout layoutRow;
    private RequestQueue mQueue;
    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        return inflater.inflate(R.layout.child_monitor_patok, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        mQueue = Volley.newRequestQueue(getContext());
        layoutRow = view.findViewById(R.id.layoutRow);
        loadTableData();
    }

    void loadTableData() {
        String url = "https://f59c-43-252-106-202.ngrok-free.app" + API.PATOK_TABLE;
        Toast.makeText(getContext(), "Loading data...", Toast.LENGTH_LONG).show();
        JsonObjectRequest request = new JsonObjectRequest(Request.Method.GET, url, null,
                response -> {
                    try {
                        JSONArray jsonArray = response.getJSONArray("data");
                        for (int i = 0; i < jsonArray.length(); i++) {
                            JSONObject jsonObject = jsonArray.getJSONObject(i);
                            String model = jsonObject.getString("fields");

                            JSONObject obj = new JSONObject(model);
                            String no = obj.getString("no_patok");
                            String afdeling = obj.getString("afd_name");
                            String block = obj.getString("block_name");
                            String latitude = obj.getString("latitude");
                            String longitude = obj.getString("longitude");
                            String periode = obj.getString("periode");
                            String status = obj.getString("status");
                            int objectid = obj.getInt("objectid");

                            addTableRow(no, afdeling, block, latitude, longitude, periode, status, objectid);
                        }
                    } catch (JSONException e) {
                        Log.i("Child Patok Monitor", e.getMessage());
                    }
                }, error -> {
            if (error instanceof TimeoutError) {
                Log.i("Child Patok Monitor", "onErrorResponse: Timeout");
                Toast.makeText(getContext(), "Time out", Toast.LENGTH_LONG).show();
            } else if (error instanceof ServerError) {
                Log.i("Child Patok Monitor", "onErrorResponse: Server error");
                Toast.makeText(getContext(), "Server error", Toast.LENGTH_LONG).show();
            } else if (error instanceof NetworkError) {
                Toast.makeText(getContext(), "Network error", Toast.LENGTH_LONG).show();
            } else if (error instanceof ParseError) {
                Log.i("Child Patok Monitor", "onErrorResponse: Parse error");
                Toast.makeText(getContext(), "Parse error", Toast.LENGTH_LONG).show();
            } else {
                Log.i("Child Patok Monitor", "onErrorResponse: Something went wrong ");
                Toast.makeText(getContext(), "Other error", Toast.LENGTH_LONG).show();
            }
        });
        request.setRetryPolicy(new DefaultRetryPolicy(15000,DefaultRetryPolicy.DEFAULT_MAX_RETRIES,DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));
        request.setShouldCache(false);
        mQueue.add(request);
    }

    void addTableRow(String no, String afdeling, String block, String latitude, String longtitude, String period, String status, int objectid) {
        TableRow tableRow = new TableRow(getContext());
        tableRow.setId(objectid);
        tableRow.addView(addTextView(no));
        tableRow.addView(addTextView(afdeling));
        tableRow.addView(addTextView(block));
        tableRow.addView(addTextView(latitude));
        tableRow.addView(addTextView(longtitude));
        tableRow.addView(addTextView(period));
        tableRow.addView(addTextView(status));
        tableRow.setLayoutParams(new TableRow.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));
        tableRow.setBackgroundColor(ContextCompat.getColor(getContext(), R.color.dashboardInfoTextBottom));
        float padding = getResources().getDimension(R.dimen.patokTableRowPadding);
        tableRow.setPadding(0, (int) padding, 0, (int) padding);
        tableRow.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //Toast.makeText(getContext(), String.valueOf(v.getId()), Toast.LENGTH_LONG).show();
            }
        });
        layoutRow.addView(tableRow);
    }

    TextView addTextView(String label) {
        TextView textView = new TextView(getContext());
        textView.setText(label);
        textView.setGravity(Gravity.CENTER);
        textView.setTextColor(ContextCompat.getColor(getContext(), R.color.textColor));
        textView.setTextSize(15);

        float width = getResources().getDimension(R.dimen.patokTableTextWidth);
        TableRow.LayoutParams params = new TableRow.LayoutParams((int) width, ViewGroup.LayoutParams.WRAP_CONTENT);
        textView.setLayoutParams(params);

        return textView;
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
    }
}
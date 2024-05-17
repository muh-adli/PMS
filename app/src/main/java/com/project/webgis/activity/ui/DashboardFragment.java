package com.project.webgis.activity.ui;

import android.os.Bundle;
import android.os.Handler;
import android.provider.ContactsContract;
import android.util.Log;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.TableRow;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.core.content.ContextCompat;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;

import com.android.volley.DefaultRetryPolicy;
import com.android.volley.NetworkError;
import com.android.volley.ParseError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.ServerError;
import com.android.volley.TimeoutError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.github.mikephil.charting.components.XAxis;
import com.github.mikephil.charting.components.YAxis;
import com.github.mikephil.charting.data.BarData;
import com.github.mikephil.charting.data.BarDataSet;
import com.github.mikephil.charting.data.BarEntry;
import com.github.mikephil.charting.formatter.IndexAxisValueFormatter;
import com.github.mikephil.charting.utils.ColorTemplate;
import com.project.webgis.API;
import com.project.webgis.R;
import com.project.webgis.adapter.DataManager;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;

public class DashboardFragment extends Fragment {
    private DataManager dataManager;
    private RequestQueue mQueue;
    private LinearLayout layoutRow;
    private String HOST;
    private ProgressBar loading;
    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_dashboard, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        dataManager = new DataManager(getContext());
        mQueue = Volley.newRequestQueue(getContext());
        layoutRow = view.findViewById(R.id.layoutRow);

        loading = view.findViewById(R.id.loading);

        HOST = dataManager.getData("HOST");

        new Handler().postDelayed(() -> {
            if (dataManager.isDataAvailable("PLANTED_HGU")) {
                loadCachePlantedData();
            } else {
                loadPlantedData();
            }
        }, 1000);

        Toast.makeText(getContext(), "Loading data...", Toast.LENGTH_LONG).show();
    }

    void loadPlantedData() {
        String url = HOST + API.PLANTED_TABLE;
        JsonObjectRequest request = new JsonObjectRequest(Request.Method.GET, url, null,
                response -> {
                    try {
                        // Data for table
                        JSONArray jsonArray = response.getJSONArray("data");
                        for (int i = 0; i < jsonArray.length(); i++) {
                            JSONObject jsonObject = jsonArray.getJSONObject(i);

                            int id = jsonObject.getInt("id");
                            String afdeling = jsonObject.getString("afd_name");
                            String block = jsonObject.getString("block_name");
                            String sap = jsonObject.getString("block_sap");
                            String ha = jsonObject.getString("ha");
                            String year = jsonObject.getString("year");
                            String level1 = jsonObject.getString("level1");
                            String level2 = jsonObject.getString("level2");
                            String status = jsonObject.getString("status");

                            addTableRow(id, afdeling, block, sap, ha, year, level1, level2, status);
                        }

                        dataManager.saveData("PLANTED_HGU", response.toString());
                        loading.setVisibility(View.GONE);
                    } catch (JSONException e) {
                        Log.i("Dashboard", e.getMessage());
                    }
                }, error -> {
            if (error instanceof TimeoutError) {
                Log.i("Dashboard", "onErrorResponse: Timeout");
                Toast.makeText(getContext(), "Time out", Toast.LENGTH_LONG).show();
            } else if (error instanceof ServerError) {
                Log.i("Dashboard", "onErrorResponse: Server error");
                Toast.makeText(getContext(), "Server error", Toast.LENGTH_LONG).show();
            } else if (error instanceof NetworkError) {
                Toast.makeText(getContext(), "Network error", Toast.LENGTH_LONG).show();
            } else if (error instanceof ParseError) {
                Log.i("Dashboard", "onErrorResponse: Parse error");
                Toast.makeText(getContext(), "Parse error", Toast.LENGTH_LONG).show();
            } else {
                Log.i("Dashboard", "onErrorResponse: Something went wrong ");
                Toast.makeText(getContext(), "Other error", Toast.LENGTH_LONG).show();
            }
        });
        request.setRetryPolicy(new DefaultRetryPolicy(15000,DefaultRetryPolicy.DEFAULT_MAX_RETRIES,DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));
        request.setShouldCache(false);
        mQueue.add(request);
    }

    void loadCachePlantedData() {
        String data = dataManager.getData("PLANTED_HGU");
        try {
            JSONObject dataObj = new JSONObject(data);

            // Data for table
            JSONArray jsonArray = dataObj.getJSONArray("data");
            for (int i = 0; i < jsonArray.length(); i++) {
                JSONObject jsonObject = jsonArray.getJSONObject(i);

                int id = jsonObject.getInt("id");
                String afdeling = jsonObject.getString("afd_name");
                String block = jsonObject.getString("block_name");
                String sap = jsonObject.getString("block_sap");
                String ha = jsonObject.getString("ha");
                String year = jsonObject.getString("year");
                String level1 = jsonObject.getString("level1");
                String level2 = jsonObject.getString("level2");
                String status = jsonObject.getString("status");

                addTableRow(id, afdeling, block, sap, ha, year, level1, level2, status);
            }
            loading.setVisibility(View.GONE);
        } catch (JSONException e) {
            Log.i("Dashboard", e.getMessage());
        }
    }

    void addTableRow(int id, String afdeling, String block, String sap, String ha, String year, String level1, String level2, String status) {
        TableRow tableRow = new TableRow(getContext());
        tableRow.setId(id);
        tableRow.addView(addTextView(afdeling));
        tableRow.addView(addTextView(block));
        tableRow.addView(addTextView(sap));
        tableRow.addView(addTextView(ha));
        tableRow.addView(addTextView(year));
        tableRow.addView(addTextView(level1));
        tableRow.addView(addTextView(level2));
        tableRow.addView(addTextView(status));
        tableRow.setLayoutParams(new TableRow.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));
        tableRow.setBackgroundColor(ContextCompat.getColor(getContext(), R.color.dashboardInfoTextBottom));
        float padding = getResources().getDimension(R.dimen.patokTableRowPadding);
        tableRow.setPadding(0, (int) padding, 0, (int) padding);
        tableRow.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(getContext(), String.valueOf(v.getId()), Toast.LENGTH_LONG).show();
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
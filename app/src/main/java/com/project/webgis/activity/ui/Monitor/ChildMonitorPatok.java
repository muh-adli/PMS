package com.project.webgis.activity.ui.Monitor;

import android.graphics.Color;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
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
import com.github.mikephil.charting.charts.BarChart;
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

public class ChildMonitorPatok extends Fragment {

    LinearLayout layoutRow;
    BarChart barChart;
    private RequestQueue mQueue;
    private DataManager dataManager;
    private ProgressBar loading;
    private String HOST;
    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        return inflater.inflate(R.layout.child_monitor_patok, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        dataManager = new DataManager(getContext());
        mQueue = Volley.newRequestQueue(getContext());
        layoutRow = view.findViewById(R.id.layoutRow);
        barChart = view.findViewById(R.id.chart);
        loading = view.findViewById(R.id.loading);

        HOST = dataManager.getData("HOST");

        new Handler().postDelayed(() -> {
            if (dataManager.isDataAvailable("PATOK_HGU")) {
                loadCachePatokData();
            } else {
                loadPatokData();
            }
        }, 1000);
    }

    void loadPatokData() {
        Log.i("Child Patok Monitor", "Downloading patok data");
        String url = HOST + API.PATOK_TABLE;
        JsonObjectRequest request = new JsonObjectRequest(Request.Method.GET, url, null,
                response -> {
                    Log.i("Child Patok Monitor", "Patok data downloaded");
                    try {

                        // Data for table
                        JSONArray jsonArray = response.getJSONArray("data");
                        for (int i = 0; i < jsonArray.length(); i++) {
                            JSONObject jsonObject = jsonArray.getJSONObject(i);

                            String no = jsonObject.getString("no_patok");
                            String afdeling = jsonObject.getString("afd_name");
                            String block = jsonObject.getString("block_name");
                            String latitude = jsonObject.getString("latitude");
                            String longitude = jsonObject.getString("longtitude");
                            String periode = jsonObject.getString("period");
                            String status = jsonObject.getString("status");
                            int id = jsonObject.getInt("id");

                            addTableRow(no, afdeling, block, latitude, longitude, periode, status, id);
                        }

                        // Data for chart
                        String chart = response.getString("chart");
                        JSONObject object = new JSONObject(chart);
                        int Q1 = object.getInt("Q1");
                        int Q2 = object.getInt("Q2");
                        int Q3 = object.getInt("Q3");
                        int Q4 = object.getInt("Q4");
                        int NA = object.getInt("N/A");

                        final String[] quart = {"Q1", "Q2", "Q3", "Q4", "N/A"};
                        XAxis xAxis = barChart.getXAxis();
                        xAxis.setValueFormatter(new IndexAxisValueFormatter(quart));
                        xAxis.setPosition(XAxis.XAxisPosition.BOTTOM);
                        xAxis.setTextColor(ContextCompat.getColor(getContext(), R.color.textColor));

                        YAxis yAxis = barChart.getAxisLeft();
                        yAxis.setTextColor(ContextCompat.getColor(getContext(), R.color.textColor));

                        ArrayList<BarEntry> barArrayList = new ArrayList<>();
                        barArrayList.add(new BarEntry(0, Q1));
                        barArrayList.add(new BarEntry(1, Q2));
                        barArrayList.add(new BarEntry(2, Q3));
                        barArrayList.add(new BarEntry(3, Q4));
                        barArrayList.add(new BarEntry(4, NA));

                        BarDataSet barDataSet = new BarDataSet(barArrayList, "Patok HGU");
                        barDataSet.setColors(ColorTemplate.COLORFUL_COLORS);
                        barDataSet.setValueTextColor(ContextCompat.getColor(getContext(), R.color.textColor));
                        barDataSet.setValueTextSize(14f);

                        BarData barData = new BarData(barDataSet);

                        barChart.setFitBars(true);
                        barChart.setData(barData);
                        barChart.getDescription().setEnabled(false);
                        barChart.getLegend().setTextColor(ContextCompat.getColor(getContext(), R.color.textColor));
                        barChart.animateXY(2000,2000);
                        barChart.invalidate();

                        dataManager.saveData("PATOK_HGU", response.toString());

                        loading.setVisibility(View.GONE);
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
                Log.i("Child Patok Monitor", "onErrorResponse: Network error");
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

    void loadCachePatokData() {
        String data = dataManager.getData("PATOK_HGU");

        try {
            JSONObject dataObj = new JSONObject(data);

            // Data for table
            JSONArray jsonArray = dataObj.getJSONArray("data");
            for (int i = 0; i < jsonArray.length(); i++) {
                JSONObject jsonObject = jsonArray.getJSONObject(i);

                String no = jsonObject.getString("no_patok");
                String afdeling = jsonObject.getString("afd_name");
                String block = jsonObject.getString("block_name");
                String latitude = jsonObject.getString("latitude");
                String longitude = jsonObject.getString("longtitude");
                String periode = jsonObject.getString("period");
                String status = jsonObject.getString("status");
                int id = jsonObject.getInt("id");

                addTableRow(no, afdeling, block, latitude, longitude, periode, status, id);
            }

            // Data for chart
            String chart = dataObj.getString("chart");
            JSONObject object = new JSONObject(chart);
            int Q1 = object.getInt("Q1");
            int Q2 = object.getInt("Q2");
            int Q3 = object.getInt("Q3");
            int Q4 = object.getInt("Q4");
            int NA = object.getInt("N/A");

            final String[] quart = {"Q1", "Q2", "Q3", "Q4", "N/A"};
            XAxis xAxis = barChart.getXAxis();
            xAxis.setValueFormatter(new IndexAxisValueFormatter(quart));
            xAxis.setPosition(XAxis.XAxisPosition.BOTTOM);
            xAxis.setTextColor(ContextCompat.getColor(getContext(), R.color.textColor));

            YAxis yAxis = barChart.getAxisLeft();
            yAxis.setTextColor(ContextCompat.getColor(getContext(), R.color.textColor));

            ArrayList<BarEntry> barArrayList = new ArrayList<>();
            barArrayList.add(new BarEntry(0, Q1));
            barArrayList.add(new BarEntry(1, Q2));
            barArrayList.add(new BarEntry(2, Q3));
            barArrayList.add(new BarEntry(3, Q4));
            barArrayList.add(new BarEntry(4, NA));

            BarDataSet barDataSet = new BarDataSet(barArrayList, "Patok HGU");
            barDataSet.setColors(ColorTemplate.COLORFUL_COLORS);
            barDataSet.setValueTextColor(ContextCompat.getColor(getContext(), R.color.textColor));
            barDataSet.setValueTextSize(14f);

            BarData barData = new BarData(barDataSet);

            barChart.setFitBars(true);
            barChart.setData(barData);
            barChart.getDescription().setEnabled(false);
            barChart.getLegend().setTextColor(ContextCompat.getColor(getContext(), R.color.textColor));
            barChart.animateXY(2000,2000);
            barChart.invalidate();

            loading.setVisibility(View.GONE);
        } catch (JSONException e) {
            Log.i("Child Patok Monitor", e.getMessage());
        }

    }

    void addTableRow(String no, String afdeling, String block, String latitude, String longtitude, String period, String status, int id) {
        TableRow tableRow = new TableRow(getContext());
        tableRow.setId(id);
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
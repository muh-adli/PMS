package com.project.webgis.activity.ui.Monitor;

import android.app.ProgressDialog;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.HorizontalScrollView;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TableRow;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AlertDialog;
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
import com.github.mikephil.charting.formatter.ValueFormatter;
import com.project.webgis.API;
import com.project.webgis.R;
import com.project.webgis.activity.ui.DumpEdit;
import com.project.webgis.adapter.DataManager;
import com.project.webgis.model.Dump;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

public class ChildMonitorTankos extends Fragment {
    LinearLayout layoutRow;
    LinearLayout headerRow;
    private LinearLayout buttonLayout;
    BarChart barChart;
    private RequestQueue mQueue;
    private DataManager dataManager;
    private String HOST;
    private ProgressDialog mProgressBar;
    private List<Dump> tankos = new ArrayList<>();
    private final int PAGE_SIZE = 50;
    private int no_of_pages;
    private Button[] buttons;
    private HorizontalScrollView scrollView;
    private Button btnAplikasi;
    private Button btnDump;
    private String loadedTable = "Aplikasi";

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        return inflater.inflate(R.layout.child_monitor_tankos, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        dataManager = new DataManager(getContext());
        mQueue = Volley.newRequestQueue(getContext());
        layoutRow = view.findViewById(R.id.layoutRow);
        headerRow = view.findViewById(R.id.headerRow);
        barChart = view.findViewById(R.id.chart);
        buttonLayout = view.findViewById(R.id.btnLay);
        scrollView = view.findViewById(R.id.horizontal_scroll_view);
        mProgressBar = new ProgressDialog(getContext());
        btnAplikasi = view.findViewById(R.id.buttonAplikasi);
        btnDump = view.findViewById(R.id.buttonDump);

        mProgressBar.setCancelable(false);
        mProgressBar.setMessage("Fetching Data...");
        mProgressBar.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        mProgressBar.show();

        HOST = dataManager.getData("HOST");

        new Handler().postDelayed(() -> {
            if (dataManager.isDataAvailable("DUMP_TABLE")) {
                if (isOnline()) {
                    loadDumpData();
                } else {
                    loadCacheDumpData();
                }
            } else {
                if (isOnline()) {
                    loadDumpData();
                } else {
                    networkUnavailable();
                }
            }

            loadChart();

        }, 1000);

        btnAplikasi.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (dataManager.isDataAvailable("APL_TABLE")) {
                    if (isOnline()) {
                        loadDumpData();
                    } else {
                        loadCacheDumpData();
                    }
                } else {
                    if (isOnline()) {
                        loadDumpData();
                    } else {
                        networkUnavailable();
                    }
                }
            }
        });

        btnDump.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (dataManager.isDataAvailable("DUMP_TABLE")) {
                    if (isOnline()) {
                        loadDumpData();
                    } else {
                        loadCacheDumpData();
                    }
                } else {
                    if (isOnline()) {
                        loadDumpData();
                    } else {
                        networkUnavailable();
                    }
                }
            }
        });
    }

    void loadDumpData() {
        Log.i("Child Tankos Monitor", "Downloading dump data");
        String url = HOST + API.DUMP_TABLE;
        JsonObjectRequest request = new JsonObjectRequest(Request.Method.GET, url, null,
                response -> {
                    Log.i("Child Tankos Monitor", "Dump data downloaded");
                    try {

                        // Data for table
                        JSONArray jsonArray = response.getJSONArray("data");
                        for (int i = 0; i < jsonArray.length(); i++) {
                            JSONObject jsonObject = jsonArray.getJSONObject(i);

                            String afdeling = jsonObject.getString("afdeling");
                            String block = jsonObject.getString("block");
                            String location = jsonObject.getString("location");
                            String dump_date = jsonObject.getString("dump_date");
                            int id = jsonObject.getInt("id");

                            tankos.add(new Dump(id, afdeling, block, location, dump_date));
                        }

                        addDumpHeader();
                        createDumpTable(tankos, 0);
                        paginateDump(buttonLayout, jsonArray.length(), PAGE_SIZE, tankos);

                        dataManager.saveData("DUMP_TABLE", response.toString());
                        mProgressBar.hide();
                    } catch (JSONException e) {
                        Log.i("Child Tankos Monitor", e.getMessage());
                        mProgressBar.hide();
                    }
                }, error -> {
            if (error instanceof TimeoutError) {
                Log.i("Child Tankos Monitor", "onErrorResponse: Timeout");
                Toast.makeText(getContext(), "Time out", Toast.LENGTH_LONG).show();
            } else if (error instanceof ServerError) {
                Log.i("Child Tankos Monitor", "onErrorResponse: Server error");
                Toast.makeText(getContext(), "Server error", Toast.LENGTH_LONG).show();
            } else if (error instanceof NetworkError) {
                Log.i("Child Tankos Monitor", "onErrorResponse: Network error");
                Toast.makeText(getContext(), "Network error", Toast.LENGTH_LONG).show();
            } else if (error instanceof ParseError) {
                Log.i("Child Tankos Monitor", "onErrorResponse: Parse error");
                Toast.makeText(getContext(), "Parse error", Toast.LENGTH_LONG).show();
            } else {
                Log.i("Child Tankos Monitor", "onErrorResponse: Something went wrong ");
                Toast.makeText(getContext(), "Other error", Toast.LENGTH_LONG).show();
            }
        });
        request.setRetryPolicy(new DefaultRetryPolicy(15000, DefaultRetryPolicy.DEFAULT_MAX_RETRIES, DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));
        request.setShouldCache(false);
        mQueue.add(request);
    }

    void loadAplData() {
        Log.i("Child Tankos Monitor", "Downloading dump data");
        String url = HOST + API.DUMP_TABLE;
        JsonObjectRequest request = new JsonObjectRequest(Request.Method.GET, url, null,
                response -> {
                    Log.i("Child Tankos Monitor", "Dump data downloaded");
                    try {

                        // Data for table
                        JSONArray jsonArray = response.getJSONArray("data");
                        for (int i = 0; i < jsonArray.length(); i++) {
                            JSONObject jsonObject = jsonArray.getJSONObject(i);

                            String afdeling = jsonObject.getString("afdeling");
                            String block = jsonObject.getString("block");
                            String location = jsonObject.getString("location");
                            String dump_date = jsonObject.getString("dump_date");
                            int id = jsonObject.getInt("id");

                            tankos.add(new Dump(id, afdeling, block, location, dump_date));
                        }

                        addDumpHeader();
                        createDumpTable(tankos, 0);
                        paginateDump(buttonLayout, jsonArray.length(), PAGE_SIZE, tankos);

                        dataManager.saveData("DUMP_TABLE", response.toString());
                        mProgressBar.hide();
                    } catch (JSONException e) {
                        Log.i("Child Tankos Monitor", e.getMessage());
                        mProgressBar.hide();
                    }
                }, error -> {
            if (error instanceof TimeoutError) {
                Log.i("Child Tankos Monitor", "onErrorResponse: Timeout");
                Toast.makeText(getContext(), "Time out", Toast.LENGTH_LONG).show();
            } else if (error instanceof ServerError) {
                Log.i("Child Tankos Monitor", "onErrorResponse: Server error");
                Toast.makeText(getContext(), "Server error", Toast.LENGTH_LONG).show();
            } else if (error instanceof NetworkError) {
                Log.i("Child Tankos Monitor", "onErrorResponse: Network error");
                Toast.makeText(getContext(), "Network error", Toast.LENGTH_LONG).show();
            } else if (error instanceof ParseError) {
                Log.i("Child Tankos Monitor", "onErrorResponse: Parse error");
                Toast.makeText(getContext(), "Parse error", Toast.LENGTH_LONG).show();
            } else {
                Log.i("Child Tankos Monitor", "onErrorResponse: Something went wrong ");
                Toast.makeText(getContext(), "Other error", Toast.LENGTH_LONG).show();
            }
        });
        request.setRetryPolicy(new DefaultRetryPolicy(15000, DefaultRetryPolicy.DEFAULT_MAX_RETRIES, DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));
        request.setShouldCache(false);
        mQueue.add(request);
    }

    private void paginateDump(final LinearLayout buttonLayout, final int data_size, final int page_size, final List<Dump> planted) {
        no_of_pages = (data_size + page_size - 1) / page_size;
        buttons = new Button[no_of_pages];
        showPageNo(0, no_of_pages);

        for (int i = 0; i < no_of_pages; i++) {
            buttons[i] = new Button(getContext());
            buttons[i].setBackgroundColor(getResources().getColor(android.R.color.transparent));
            buttons[i].setText(String.valueOf(i + 1));

            LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT);
            buttonLayout.addView(buttons[i], lp);

            final int j = i;
            buttons[j].setOnClickListener(new View.OnClickListener() {

                public void onClick(View v) {
                    scrollView.fullScroll(ScrollView.FOCUS_UP);
                    createDumpTable(tankos, j);
                    checkBtnBackGroud(j);
                    showPageNo(j, no_of_pages);
                }
            });
        }
        checkBtnBackGroud(0);
    }

    private void showPageNo(int j, int no_of_pages) {
        Toast.makeText(getContext(), "Page " + (j + 1) + " of " + no_of_pages, Toast.LENGTH_LONG).show();
    }

    private void checkBtnBackGroud(int index) {
        for (int i = 0; i < no_of_pages; i++) {
            if (i == index) {
                buttons[index].setBackgroundResource(R.drawable.cell_shape_square_green);
            } else {
                buttons[i].setBackground(null);
            }
        }
    }

    private void createDumpTable(List<Dump> planted, int page) {
        layoutRow.removeAllViews();
        // data rows
        for (int i = 0, j = page * PAGE_SIZE; j < planted.size() && i < PAGE_SIZE; i++, j++) {
            addDumpTableRow(
                    planted.get(j).getId(),
                    planted.get(j).getAfdeling(),
                    planted.get(j).getBlock(),
                    planted.get(j).getLocation(),
                    planted.get(j).getDump_date(),
                    i,
                    j
            );
        }

    }

    void loadCacheDumpData() {
        String data = dataManager.getData("DUMP_TABLE");

        try {
            JSONObject dataObj = new JSONObject(data);

            // Data for table
            JSONArray jsonArray = dataObj.getJSONArray("data");
            for (int i = 0; i < jsonArray.length(); i++) {
                JSONObject jsonObject = jsonArray.getJSONObject(i);

                String afdeling = jsonObject.getString("afdeling");
                String block = jsonObject.getString("block");
                String location = jsonObject.getString("location");
                String dump_date = jsonObject.getString("dump_date");
                int id = jsonObject.getInt("id");
                tankos.add(new Dump(id, afdeling, block, location, dump_date));
            }

            createDumpTable(tankos, 0);
            paginateDump(buttonLayout, jsonArray.length(), PAGE_SIZE, tankos);

            mProgressBar.hide();

        } catch (JSONException e) {
            Log.i("Child Tankos Monitor", e.getMessage());
            mProgressBar.hide();
        }

    }

    void addDumpHeader() {
        headerRow.removeAllViews();
        TableRow tableRow = new TableRow(getContext());
        tableRow.addView(addTextView("Afdeling"));
        tableRow.addView(addTextView("Block"));
        tableRow.addView(addTextView("Location"));
        tableRow.addView(addTextView("Date"));
        tableRow.setLayoutParams(new TableRow.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));
        float padding = getResources().getDimension(R.dimen.patokTableRowPadding);
        tableRow.setPadding(0, (int) padding, 0, (int) padding);
        tableRow.setBackgroundColor(ContextCompat.getColor(getContext(), R.color.dashboardInfoTextTop));

        headerRow.addView(tableRow);
    }

    void addDumpTableRow(int id, String afdeling, String block, String location, String dump_date, int index, int index2) {
        TableRow tableRow = new TableRow(getContext());
        tableRow.setId(id);
        tableRow.addView(addTextView(afdeling));
        tableRow.addView(addTextView(block));
        tableRow.addView(addTextView(location));
        tableRow.addView(addTextView(dump_date));
        tableRow.setLayoutParams(new TableRow.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));
        float padding = getResources().getDimension(R.dimen.patokTableRowPadding);
        tableRow.setPadding(0, (int) padding, 0, (int) padding);
        tableRow.setBackgroundColor(ContextCompat.getColor(getContext(), R.color.dashboardInfoTextBottom));

        tableRow.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(getContext(), DumpEdit.class);
                intent.putExtra("id", tankos.get(index2).getId());
                intent.putExtra("afdeling", tankos.get(index2).getAfdeling());
                intent.putExtra("block", tankos.get(index2).getBlock());
                intent.putExtra("location", tankos.get(index2).getLocation());
                intent.putExtra("dump_date", tankos.get(index2).getDump_date());
                startActivity(intent);
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

    private void loadChart() {
        if (isOnline()) {
            Log.i("Child Tankos Monitor", "Downloading tankos chart data");
            String url = HOST + API.TANKOS_CHART;
            JsonObjectRequest request = new JsonObjectRequest(Request.Method.GET, url, null,
                    response -> {
                        Log.i("Child Tankos Monitor", "Tankos chart data downloaded");
                        try {
                            dataManager.saveData("TANKOS_CHART", response.getString("chart"));

                            String chart = response.getString("chart");

                            JSONObject object = new JSONObject(chart);
                            JSONArray date = object.getJSONArray("date");
                            JSONArray pokok = object.getJSONArray("pokok");
                            JSONArray tonase = object.getJSONArray("tonase");
                            JSONArray dump = object.getJSONArray("dump");

                            float groupSpace = 0.1f;
                            float barSpace = 0.03f; // x2 dataset
                            float barWidth = 0.40f; // x2 dataset
                            int groupCount = date.length();

                            final ArrayList<String> quart = new ArrayList<>();
                            for (int i = 0; i < date.length(); i++) {
                                quart.add(date.getString(i));
                            }

                            XAxis xAxis = barChart.getXAxis();
                            xAxis.setValueFormatter(new IndexAxisValueFormatter(quart));
                            xAxis.setDrawGridLines(false);
                            xAxis.setDrawAxisLine(false);
                            xAxis.setPosition(XAxis.XAxisPosition.BOTTOM);
                            xAxis.setAxisMinimum(0f);
                            xAxis.setGranularity(1);
                            xAxis.setCenterAxisLabels(true);
                            xAxis.setAxisMaximum(date.length());
                            xAxis.setTextColor(ContextCompat.getColor(getContext(), R.color.textColor));

                            YAxis yAxis = barChart.getAxisLeft();
                            yAxis.setTextColor(ContextCompat.getColor(getContext(), R.color.textColor));

                            List<BarEntry> pokokArrayList = new ArrayList<>();
                            for (int i = 0; i < pokok.length(); i++) {
                                pokokArrayList.add(new BarEntry(i, pokok.getInt(i)));
                            }

                            List<BarEntry> tonaseArrayList = new ArrayList<>();
                            for (int i = 0; i < tonase.length(); i++) {
                                tonaseArrayList.add(new BarEntry(i, tonase.getInt(i)));
                            }

                            List<BarEntry> dumpArrayList = new ArrayList<>();
                            for (int i = 0; i < dump.length(); i++) {
                                dumpArrayList.add(new BarEntry(i, dump.getInt(i)));
                            }

                            BarDataSet pokokDataSet = new BarDataSet(pokokArrayList, "Pokok");
                            pokokDataSet.setColors(Color.rgb(62, 134, 240));
                            pokokDataSet.setValueTextColor(ContextCompat.getColor(getContext(), R.color.textColor));
                            pokokDataSet.setValueTextSize(12f);

                            BarDataSet tonaseDataSet = new BarDataSet(tonaseArrayList, "Tonase");
                            tonaseDataSet.setColors(Color.rgb(242, 209, 0));
                            tonaseDataSet.setValueTextColor(ContextCompat.getColor(getContext(), R.color.textColor));
                            tonaseDataSet.setValueTextSize(12f);

                            BarDataSet dumpDataSet = new BarDataSet(dumpArrayList, "Dump");
                            dumpDataSet.setColors(Color.rgb(19, 171, 69));
                            dumpDataSet.setValueTextColor(ContextCompat.getColor(getContext(), R.color.textColor));
                            dumpDataSet.setValueTextSize(12f);

                            BarData barData = new BarData(pokokDataSet, tonaseDataSet, dumpDataSet);
                            barData.setBarWidth(barWidth);

                            ValueFormatter vf = new ValueFormatter() {
                                @Override
                                public String getFormattedValue(float value) {
                                    return "" + (int) value;
                                }
                            };
                            barData.setValueFormatter(vf);

                            barChart.setFitBars(true);
                            barChart.setData(barData);
                            barChart.getXAxis().setAxisMinimum(0);
                            //barChart.getXAxis().setAxisMaximum(0 + barChart.getBarData().getGroupWidth(groupSpace, barSpace) * groupCount);
                            barChart.groupBars(0, groupSpace, barSpace); // perform the "explicit" grouping
                            barChart.getDescription().setEnabled(false);
                            barChart.getLegend().setTextColor(ContextCompat.getColor(getContext(), R.color.textColor));
                            barChart.animateXY(2000, 2000);
                            barChart.invalidate();
                        } catch (JSONException e) {
                            Log.i("Child Tankos Monitor", e.getMessage());
                            mProgressBar.hide();
                        }
                    }, error -> {
                if (error instanceof TimeoutError) {
                    Log.i("Child Tankos Monitor", "onErrorResponse: Timeout");
                    Toast.makeText(getContext(), "Time out", Toast.LENGTH_LONG).show();
                } else if (error instanceof ServerError) {
                    Log.i("Child Tankos Monitor", "onErrorResponse: Server error");
                    Toast.makeText(getContext(), "Server error", Toast.LENGTH_LONG).show();
                } else if (error instanceof NetworkError) {
                    Log.i("Child Tankos Monitor", "onErrorResponse: Network error");
                    Toast.makeText(getContext(), "Network error", Toast.LENGTH_LONG).show();
                } else if (error instanceof ParseError) {
                    Log.i("Child Tankos Monitor", "onErrorResponse: Parse error");
                    Toast.makeText(getContext(), "Parse error", Toast.LENGTH_LONG).show();
                } else {
                    Log.i("Child Tankos Monitor", "onErrorResponse: Something went wrong ");
                    Toast.makeText(getContext(), "Other error", Toast.LENGTH_LONG).show();
                }
            });
            request.setRetryPolicy(new DefaultRetryPolicy(15000, DefaultRetryPolicy.DEFAULT_MAX_RETRIES, DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));
            request.setShouldCache(false);
            mQueue.add(request);
        } else if (!isOnline() && dataManager.isDataAvailable("TANKOS_CHART")) {
            String chart = dataManager.getData("TANKOS_CHART");
            try {
                JSONObject object = new JSONObject(chart);
                JSONArray date = object.getJSONArray("date");
                JSONArray pokok = object.getJSONArray("pokok");
                JSONArray tonase = object.getJSONArray("tonase");
                JSONArray dump = object.getJSONArray("dump");

                float groupSpace = 0.1f;
                float barSpace = 0.03f; // x2 dataset
                float barWidth = 0.40f; // x2 dataset
                int groupCount = date.length();

                final ArrayList<String> quart = new ArrayList<>();
                for (int i = 0; i < date.length(); i++) {
                    quart.add(date.getString(i));
                }

                XAxis xAxis = barChart.getXAxis();
                xAxis.setValueFormatter(new IndexAxisValueFormatter(quart));
                xAxis.setDrawGridLines(false);
                xAxis.setDrawAxisLine(false);
                xAxis.setPosition(XAxis.XAxisPosition.BOTTOM);
                xAxis.setAxisMinimum(0f);
                xAxis.setGranularity(1);
                xAxis.setCenterAxisLabels(true);
                xAxis.setAxisMaximum(date.length());
                xAxis.setTextColor(ContextCompat.getColor(getContext(), R.color.textColor));

                YAxis yAxis = barChart.getAxisLeft();
                yAxis.setTextColor(ContextCompat.getColor(getContext(), R.color.textColor));

                List<BarEntry> pokokArrayList = new ArrayList<>();
                for (int i = 0; i < pokok.length(); i++) {
                    pokokArrayList.add(new BarEntry(i, pokok.getInt(i)));
                }

                List<BarEntry> tonaseArrayList = new ArrayList<>();
                for (int i = 0; i < tonase.length(); i++) {
                    tonaseArrayList.add(new BarEntry(i, tonase.getInt(i)));
                }

                List<BarEntry> dumpArrayList = new ArrayList<>();
                for (int i = 0; i < dump.length(); i++) {
                    dumpArrayList.add(new BarEntry(i, dump.getInt(i)));
                }

                BarDataSet pokokDataSet = new BarDataSet(pokokArrayList, "Pokok");
                pokokDataSet.setColors(Color.rgb(62, 134, 240));
                pokokDataSet.setValueTextColor(ContextCompat.getColor(getContext(), R.color.textColor));
                pokokDataSet.setValueTextSize(12f);

                BarDataSet tonaseDataSet = new BarDataSet(tonaseArrayList, "Tonase");
                tonaseDataSet.setColors(Color.rgb(242, 209, 0));
                tonaseDataSet.setValueTextColor(ContextCompat.getColor(getContext(), R.color.textColor));
                tonaseDataSet.setValueTextSize(12f);

                BarDataSet dumpDataSet = new BarDataSet(dumpArrayList, "Dump");
                dumpDataSet.setColors(Color.rgb(19, 171, 69));
                dumpDataSet.setValueTextColor(ContextCompat.getColor(getContext(), R.color.textColor));
                dumpDataSet.setValueTextSize(12f);

                BarData barData = new BarData(pokokDataSet, tonaseDataSet, dumpDataSet);
                barData.setBarWidth(barWidth);

                ValueFormatter vf = new ValueFormatter() {
                    @Override
                    public String getFormattedValue(float value) {
                        return "" + (int) value;
                    }
                };
                barData.setValueFormatter(vf);

                barChart.setFitBars(true);
                barChart.setData(barData);
                barChart.getXAxis().setAxisMinimum(0);
                //barChart.getXAxis().setAxisMaximum(0 + barChart.getBarData().getGroupWidth(groupSpace, barSpace) * groupCount);
                barChart.groupBars(0, groupSpace, barSpace); // perform the "explicit" grouping
                barChart.getDescription().setEnabled(false);
                barChart.getLegend().setTextColor(ContextCompat.getColor(getContext(), R.color.textColor));
                barChart.animateXY(2000, 2000);
                barChart.invalidate();
            } catch (JSONException e) {
                e.printStackTrace();
            }
        } else {
            networkUnavailable();
        }
    }

    public boolean isOnline() {
        ConnectivityManager cm = (ConnectivityManager) getContext().getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo netInfo = cm.getActiveNetworkInfo();
        return netInfo != null && netInfo.isConnectedOrConnecting();
    }

    private void networkUnavailable() {
        AlertDialog.Builder builder = new AlertDialog.Builder(getContext());
        builder.setTitle("Network unavailable");
        builder.setMessage("Please connect to internet to loading data");
        builder.show();
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
    }
}
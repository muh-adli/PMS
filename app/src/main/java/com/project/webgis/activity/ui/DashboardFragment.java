package com.project.webgis.activity.ui;

import android.app.ProgressDialog;
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
import com.project.webgis.adapter.DataManager;
import com.project.webgis.model.Planted;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

public class DashboardFragment extends Fragment {
    private DataManager dataManager;
    private RequestQueue mQueue;
    private ProgressDialog mProgressBar;
    private List<Planted> planted = new ArrayList<>();
    private LinearLayout buttonLayout;
    private LinearLayout layoutRow;
    private String HOST;
    private final int PAGE_SIZE = 50;
    private int no_of_pages;
    private Button[] buttons;
    private HorizontalScrollView scrollView;

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_dashboard, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        dataManager = new DataManager(getContext());
        mQueue = Volley.newRequestQueue(getContext());

        HOST = dataManager.getData("HOST");

        mProgressBar = new ProgressDialog(getContext());
        buttonLayout = view.findViewById(R.id.btnLay);
        scrollView = view.findViewById(R.id.horizontal_scroll_view);
        layoutRow = view.findViewById(R.id.layoutRow);

        new Handler().postDelayed(() -> {
            if (dataManager.isDataAvailable("PLANTED_HGU")) {
                loadCachePlantedData();
            } else {
                loadPlantedData();
            }
        }, 1000);
    }

    void loadPlantedData() {
        mProgressBar.setCancelable(false);
        mProgressBar.setMessage("Fetching Data...");
        mProgressBar.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        mProgressBar.show();

        Log.i("Dashboard", "Downloading planted data");
        String url = HOST + API.PLANTED_TABLE;
        JsonObjectRequest request = new JsonObjectRequest(Request.Method.GET, url, null,
                response -> {
                    Log.i("Dashboard", "Planted data downloaded");
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

                            planted.add(new Planted(id, afdeling, block, sap, ha, year, level1, level2, status));
                        }

                        dataManager.saveData("PLANTED_HGU", response.toString());

                        createTable(planted, 0);
                        paginate(buttonLayout, jsonArray.length(), PAGE_SIZE, planted);

                        mProgressBar.hide();
                    } catch (JSONException e) {
                        Log.i("Dashboard", e.getMessage());
                        mProgressBar.hide();
                    }
                }, error -> {
            if (error instanceof TimeoutError) {
                Log.i("Dashboard", "onErrorResponse: Timeout");
                Toast.makeText(getContext(), "Time out", Toast.LENGTH_LONG).show();
            } else if (error instanceof ServerError) {
                Log.i("Dashboard", "onErrorResponse: Server error");
                Toast.makeText(getContext(), "Server error", Toast.LENGTH_LONG).show();
            } else if (error instanceof NetworkError) {
                Log.i("Dashboard", "Network error");
                Toast.makeText(getContext(), "Network error", Toast.LENGTH_LONG).show();
            } else if (error instanceof ParseError) {
                Log.i("Dashboard", "onErrorResponse: Parse error");
                Toast.makeText(getContext(), "Parse error", Toast.LENGTH_LONG).show();
            } else {
                Log.i("Dashboard", "onErrorResponse: Something went wrong ");
                Toast.makeText(getContext(), "Other error", Toast.LENGTH_LONG).show();
            }
        });
        request.setRetryPolicy(new DefaultRetryPolicy(15000, DefaultRetryPolicy.DEFAULT_MAX_RETRIES, DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));
        request.setShouldCache(false);
        mQueue.add(request);
    }

    private void paginate(final LinearLayout buttonLayout, final int data_size, final int page_size, final List<Planted> planted) {
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
                    createTable(planted, j);
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
                buttons[index].setBackgroundResource(R.drawable.cell_shape_square_blue);
            } else {
                buttons[i].setBackground(null);
            }
        }
    }

    private void createTable(List<Planted> planted, int page) {
        layoutRow.removeAllViews();
        // data rows
        for (int i = 0, j = page * PAGE_SIZE; j < planted.size() && i < PAGE_SIZE; i++, j++) {
            addTableRow(
                    planted.get(j).getId(),
                    planted.get(j).getAfdeling(),
                    planted.get(j).getBlock(),
                    planted.get(j).getSap(),
                    planted.get(j).getHa(),
                    planted.get(j).getYear(),
                    planted.get(j).getLevel1(),
                    planted.get(j).getLevel2(),
                    planted.get(j).getStatus(),
                    i
            );
        }

    }

    void loadCachePlantedData() {
        mProgressBar.setCancelable(false);
        mProgressBar.setMessage("Fetching Data...");
        mProgressBar.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        mProgressBar.show();

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

                planted.add(new Planted(id, afdeling, block, sap, ha, year, level1, level2, status));
            }

            createTable(planted, 0);
            paginate(buttonLayout, jsonArray.length(), PAGE_SIZE, planted);

            mProgressBar.hide();
        } catch (JSONException e) {
            Log.i("Dashboard", e.getMessage());
            mProgressBar.hide();
        }
    }

    private void addTableRow(int id, String afdeling, String block, String sap, String ha, String year, String level1, String level2, String status, int index) {
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
        if (index == -1) {
            tableRow.setBackgroundColor(ContextCompat.getColor(getContext(), R.color.dashboardInfoTextTop));
        } else {
            tableRow.setBackgroundColor(ContextCompat.getColor(getContext(), R.color.dashboardInfoTextBottom));
        }
        float padding = getResources().getDimension(R.dimen.patokTableRowPadding);
        tableRow.setPadding(0, (int) padding, 0, (int) padding);
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
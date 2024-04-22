package com.project.webgis.activity;

import android.content.IntentFilter;
import android.os.Bundle;
import android.view.MenuItem;
import android.widget.Toast;

import com.google.android.material.bottomnavigation.BottomNavigationView;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;

import com.google.android.material.navigation.NavigationBarView;
import com.project.webgis.R;
import com.project.webgis.activity.ui.dashboard.DashboardFragment;
import com.project.webgis.activity.ui.map.MapFragment;
import com.project.webgis.activity.ui.monitor.MonitorFragment;
import com.project.webgis.adapter.NetworkReceiver;

public class MainActivity extends AppCompatActivity {

    final Fragment fragmentDashboard = new DashboardFragment();
    final Fragment fragmentMap = new MapFragment();
    final Fragment fragmentMonitor = new MonitorFragment();
    final Fragment fragmentOther = new DashboardFragment();
    private Fragment active = fragmentDashboard;
    private boolean firstDashboard = true;
    private boolean firstMap = true;
    private boolean firstMonitor = true;
    private boolean firstOther = true;
    final FragmentManager fm = getSupportFragmentManager();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_main);

        IntentFilter filter = new IntentFilter();
        filter.addAction("android.net.conn.CONNECTIVITY_CHANGE");
        registerReceiver(new NetworkReceiver(), filter);

        fm.beginTransaction().add(R.id.fragment_container, fragmentDashboard).commit();

        BottomNavigationView navView = findViewById(R.id.bottomNavigation);

        navView.setOnItemSelectedListener(new NavigationBarView.OnItemSelectedListener() {
            @Override
            public boolean onNavigationItemSelected(@NonNull MenuItem menuItem) {
                int itemId = menuItem.getItemId();
                if (itemId == R.id.menu_dashboard) {
                    fm.beginTransaction().hide(active).show(fragmentDashboard).commit();
                    active = fragmentDashboard;
                    Toast.makeText(getApplicationContext(), "Dashboard", Toast.LENGTH_SHORT).show();
                    return true;
                } else if (itemId == R.id.menu_map) {
                    if (firstMap) {
                        fm.beginTransaction().add(R.id.fragment_container, fragmentMap).hide(active).commit();
                        firstMap = false;
                    } else {
                        fm.beginTransaction().hide(active).show(fragmentMap).commit();
                    }
                    active = fragmentMap;
                    Toast.makeText(getApplicationContext(), "Map", Toast.LENGTH_SHORT).show();
                    return true;
                } else if (itemId == R.id.menu_monitor) {
                    if (firstMonitor) {
                        fm.beginTransaction().add(R.id.fragment_container, fragmentMonitor).hide(active).commit();
                        firstMonitor = false;
                    } else {
                        fm.beginTransaction().hide(active).show(fragmentMonitor).commit();
                    }
                    active = fragmentMonitor;
                    Toast.makeText(getApplicationContext(), "Monitor", Toast.LENGTH_SHORT).show();
                    return true;
                } else if (itemId == R.id.menu_other) {
                    if (firstOther) {
                        fm.beginTransaction().add(R.id.fragment_container, fragmentOther).hide(active).commit();
                        firstOther = false;
                    } else {
                        fm.beginTransaction().hide(active).show(fragmentOther).commit();
                    }
                    active = fragmentOther;
                    Toast.makeText(getApplicationContext(), "Other", Toast.LENGTH_SHORT).show();
                    return true;
                }
                return false;
            }
        });

    }

    @Override
    protected void onStop() {
        super.onStop();
        unregisterReceiver(new NetworkReceiver());
    }

    @Override
    public void onDetachedFromWindow() {
        super.onDetachedFromWindow();
        unregisterReceiver(new NetworkReceiver());
    }
}
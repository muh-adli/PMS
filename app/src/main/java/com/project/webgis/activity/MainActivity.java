package com.project.webgis.activity;

import android.Manifest;
import android.content.IntentFilter;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.view.MenuItem;

import com.google.android.material.bottomnavigation.BottomNavigationView;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;

import com.google.android.material.navigation.NavigationBarView;
import com.project.webgis.R;
import com.project.webgis.activity.ui.Dashboard.DashboardFragment;
import com.project.webgis.activity.ui.MapFragment;
import com.project.webgis.activity.ui.Monitor.MonitorFragment;
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

        if (ContextCompat.checkSelfPermission(MainActivity.this,
                Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED){
            if (ActivityCompat.shouldShowRequestPermissionRationale(MainActivity.this,
                    Manifest.permission.ACCESS_FINE_LOCATION)){
                ActivityCompat.requestPermissions(MainActivity.this,
                        new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, 1);
            }else{
                ActivityCompat.requestPermissions(MainActivity.this,
                        new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, 1);
            }
        }

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
                    return true;
                } else if (itemId == R.id.menu_map) {
                    if (firstMap) {
                        fm.beginTransaction().add(R.id.fragment_container, fragmentMap).hide(active).commit();
                        firstMap = false;
                    } else {
                        fm.beginTransaction().hide(active).show(fragmentMap).commit();
                    }
                    active = fragmentMap;
                    return true;
                } else if (itemId == R.id.menu_monitor) {
                    if (firstMonitor) {
                        fm.beginTransaction().add(R.id.fragment_container, fragmentMonitor).hide(active).commit();
                        firstMonitor = false;
                    } else {
                        fm.beginTransaction().hide(active).show(fragmentMonitor).commit();
                    }
                    active = fragmentMonitor;
                    return true;
                } else if (itemId == R.id.menu_other) {
                    if (firstOther) {
                        fm.beginTransaction().add(R.id.fragment_container, fragmentOther).hide(active).commit();
                        firstOther = false;
                    } else {
                        fm.beginTransaction().hide(active).show(fragmentOther).commit();
                    }
                    active = fragmentOther;
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

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions,
                                           int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
    }
}
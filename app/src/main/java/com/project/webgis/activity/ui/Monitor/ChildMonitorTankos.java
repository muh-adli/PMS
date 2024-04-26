package com.project.webgis.activity.ui.Monitor;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;

import com.project.webgis.R;

public class ChildMonitorTankos extends Fragment {

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        return inflater.inflate(R.layout.child_monitor_tankos, container, false);
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
    }
}
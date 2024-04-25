package com.project.webgis.activity.ui.Dashboard;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;

import com.project.webgis.R;

public class ChildDashboardGeometry extends Fragment {

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        return inflater.inflate(R.layout.child_dashboard_geometry, container, false);
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
    }
}
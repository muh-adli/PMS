package com.project.webgis.activity.ui.Dashboard;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;

import com.project.webgis.R;

public class DashboardFragment extends Fragment {

    final Fragment childGeometry = new ChildDashboardGeometry();
    final Fragment childTable = new ChildDashboardTable();
    private Fragment active = childGeometry;
    private Button btnGeometry, btnTable = null;
    private boolean firstTable = true;
    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_dashboard, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        FragmentManager fm = getChildFragmentManager();

        fm.beginTransaction().add(R.id.child_fragment_container, childGeometry).commit();

        btnGeometry = (Button) view.findViewById(R.id.buttonGeometry);
        btnTable = (Button) view.findViewById(R.id.buttonTable);

        btnGeometry.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (active != childGeometry) {
                    fm.beginTransaction().hide(active).show(childGeometry).commit();
                    active = childGeometry;
                }
            }
        });

        btnTable.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (active != childTable) {
                    if (firstTable) {
                        fm.beginTransaction().add(R.id.child_fragment_container, childTable).hide(active).commit();
                        firstTable = false;
                    } else {
                        fm.beginTransaction().hide(active).show(childTable).commit();
                    }
                    active = childTable;
                }
            }
        });
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
    }
}
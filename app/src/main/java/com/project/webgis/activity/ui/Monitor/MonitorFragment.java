package com.project.webgis.activity.ui.Monitor;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.lifecycle.ViewModelProvider;

import com.project.webgis.R;


public class MonitorFragment extends Fragment {

    final Fragment childTankos = new ChildMonitorTankos();
    final Fragment childPatok = new ChildMonitorPatok();
    final Fragment childPupuk = new ChildMonitorPupuk();
    private Button btnTankos, btnPupuk, btnPatok = null;
    private boolean firstPatok = true;
    private boolean firstPupuk = true;
    private Fragment active = childTankos;

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_monitor, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        FragmentManager fm = getChildFragmentManager();

        fm.beginTransaction().add(R.id.child_fragment_container, childTankos).commit();

        btnTankos = (Button) view.findViewById(R.id.buttonTankos);
        btnPatok = (Button) view.findViewById(R.id.buttonPatok);
        btnPupuk = (Button) view.findViewById(R.id.buttonPupuk);

        btnTankos.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (active != childTankos) {
                    fm.beginTransaction().hide(active).show(childTankos).commit();
                    active = childTankos;
                }

            }
        });

        btnPatok.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (active != childPatok) {
                    if (firstPatok) {
                        fm.beginTransaction().add(R.id.child_fragment_container, childPatok).hide(active).commit();
                        firstPatok = false;
                    } else {
                        fm.beginTransaction().hide(active).show(childPatok).commit();
                    }
                    active = childPatok;
                }

            }
        });

        btnPupuk.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (active != childPupuk) {
                    if (firstPupuk) {
                        fm.beginTransaction().add(R.id.child_fragment_container, childPupuk).hide(active).commit();
                        firstPupuk = false;
                    } else {
                        fm.beginTransaction().hide(active).show(childPupuk).commit();
                    }
                    active = childPupuk;
                }

            }
        });
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
    }
}
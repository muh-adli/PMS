package com.project.webgis.activity.ui.monitor;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

public class MonitorViewModel extends ViewModel {

    private final MutableLiveData<String> mText;

    public MonitorViewModel() {
        mText = new MutableLiveData<>();
        mText.setValue("This is notifications fragment");
    }

    public LiveData<String> getText() {
        return mText;
    }
}
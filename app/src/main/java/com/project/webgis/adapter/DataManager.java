package com.project.webgis.adapter;

import android.annotation.SuppressLint;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;

import com.project.webgis.activity.MainActivity;

import java.util.HashMap;

public class DataManager {
    // Shared Preferences
    SharedPreferences pref;
    // Editor for Shared preferences
    SharedPreferences.Editor editor;
    // Context
    Context _context;
    // Shared pref mode
    int PRIVATE_MODE = 0;
    // Sharedpref file name
    private static final String PREF_NAME = "DataManager";

    // Constructor
    @SuppressLint("CommitPrefEdits")
    public DataManager(Context context) {
        this._context = context;
        pref = _context.getSharedPreferences(PREF_NAME, PRIVATE_MODE);
        editor = pref.edit();
    }

    /**
     * Save data
     */
    public void saveData(String key, String data) {
        editor.putString(key, data);
        editor.commit();
    }

    /**
     *
     * Get data
     */
    public String getData(String key) {
        return pref.getString(key, null);
    }

    /**
     * Quick check for data
     **/
    public boolean isDataAvailable(String key) {
        String data = pref.getString(key, null);
        return data != null;
    }
}
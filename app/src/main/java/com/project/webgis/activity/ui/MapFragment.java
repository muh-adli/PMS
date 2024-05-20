package com.project.webgis.activity.ui;

import android.app.ProgressDialog;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.os.Handler;
import android.preference.PreferenceManager;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.content.res.AppCompatResources;
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
import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.project.webgis.API;
import com.project.webgis.R;
import com.project.webgis.adapter.DataManager;

import org.osmdroid.api.IMapController;
import org.osmdroid.bonuspack.kml.KmlDocument;
import org.osmdroid.bonuspack.kml.Style;
import org.osmdroid.config.Configuration;
import org.osmdroid.tileprovider.tilesource.TileSourceFactory;
import org.osmdroid.util.GeoPoint;
import org.osmdroid.views.MapView;
import org.osmdroid.views.overlay.FolderOverlay;
import org.osmdroid.views.overlay.compass.CompassOverlay;
import org.osmdroid.views.overlay.compass.InternalCompassOrientationProvider;
import org.osmdroid.views.overlay.gestures.RotationGestureOverlay;
import org.osmdroid.views.overlay.mylocation.GpsMyLocationProvider;
import org.osmdroid.views.overlay.mylocation.MyLocationNewOverlay;

public class MapFragment extends Fragment {

    private MapView map = null;
    private MyLocationNewOverlay mLocationOverlay;
    private RotationGestureOverlay mRotationGestureOverlay;
    private CompassOverlay mCompassOverlay;
    private IMapController mapController;
    private RequestQueue mQueue;
    private DataManager dataManager;
    private String HOST;
    private FloatingActionButton layerButton;
    private ProgressDialog mProgress;

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_map, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        mQueue = Volley.newRequestQueue(getContext());

        dataManager = new DataManager(getContext());

        HOST = dataManager.getData("HOST");

        layerButton = view.findViewById(R.id.layerButton);
        mProgress = new ProgressDialog(getActivity());

        Context ctx = getContext();
        Configuration.getInstance().load(ctx, PreferenceManager.getDefaultSharedPreferences(ctx));

        Bitmap arrowMap = BitmapFactory.decodeResource(getResources(), org.osmdroid.library.R.drawable.round_navigation_white_48);

        map = (MapView) view.findViewById(R.id.map);
        map.setTileSource(TileSourceFactory.MAPNIK);

        map.setMultiTouchControls(true);

        /*this.mLocationOverlay = new MyLocationNewOverlay(new GpsMyLocationProvider(getActivity()), map);
        this.mLocationOverlay.enableMyLocation();
        this.mLocationOverlay.enableFollowLocation();
        this.mLocationOverlay.setDrawAccuracyEnabled(false);
        this.mLocationOverlay.setPersonIcon(arrowMap);
        map.getOverlays().add(this.mLocationOverlay);*/

        mapController = map.getController();
        mapController.setZoom(13);
        mapController.setCenter(new GeoPoint(1.2098191417100188, 117.90810018140084));

        this.mCompassOverlay = new CompassOverlay(getActivity(), new InternalCompassOrientationProvider(getActivity()), map);
        this.mCompassOverlay.enableCompass();
        map.getOverlays().add(this.mCompassOverlay);

        mProgress.setCancelable(false);
        mProgress.setMessage("Fetching Map...");
        mProgress.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        mProgress.show();

        new Handler().postDelayed(() -> {
            if (dataManager.isDataAvailable("MAP_BLOCK") && dataManager.isDataAvailable("MAP_DUMP")) {
                loadCachedOverlay();
            } else {
                loadBlockBoundary();
                loadDumpBoundary();
            }
        }, 1000);
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
    }

    @Override
    public void onResume() {
        super.onResume();
        map.onResume();
    }

    @Override
    public void onPause() {
        super.onPause();
        map.onPause();
    }

    private void loadBlockBoundary() {
        Log.i("Map Fragment", "Downloading block boundary");
        String url = HOST + API.BLOCK_BOUNDARY;
        JsonObjectRequest request = new JsonObjectRequest(Request.Method.GET, url, null,
                response -> {
                    Log.i("Map Fragment", "Block boundary downloaded");

                    KmlDocument kmlDocument = new KmlDocument();
                    kmlDocument.parseGeoJSON(response.toString());
                    Style defaultStyle = new Style(null, 0x901010AA, 5f, 0x20AA1010);
                    FolderOverlay overlay = (FolderOverlay) kmlDocument.mKmlRoot.buildOverlay(map, defaultStyle, null, kmlDocument);
                    map.getOverlays().add(overlay);

                    dataManager.saveData("MAP_BLOCK", response.toString());
                }, error -> {
            if (error instanceof TimeoutError) {
                Log.i("Map Fragment", "onErrorResponse: Timeout");
                Toast.makeText(getContext(), "Time out", Toast.LENGTH_LONG).show();
            } else if (error instanceof ServerError) {
                Log.i("Map Fragment", "onErrorResponse: Server error");
                Toast.makeText(getContext(), "Server error", Toast.LENGTH_LONG).show();
            } else if (error instanceof NetworkError) {
                Log.i("Map Fragment", "onErrorResponse: Network error");
                Toast.makeText(getContext(), "Network error", Toast.LENGTH_LONG).show();
            } else if (error instanceof ParseError) {
                Log.i("Map Fragment", "onErrorResponse: Parse error");
                Toast.makeText(getContext(), "Parse error", Toast.LENGTH_LONG).show();
            } else {
                Log.i("Map Fragment", "onErrorResponse: Something went wrong ");
                Toast.makeText(getContext(), "Other error", Toast.LENGTH_LONG).show();
            }
        });
        request.setRetryPolicy(new DefaultRetryPolicy(15000, DefaultRetryPolicy.DEFAULT_MAX_RETRIES, DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));
        request.setShouldCache(false);
        mQueue.add(request);
    }

    private void loadDumpBoundary() {
        Log.i("Map Fragment", "Downloading dump boundary");
        String url = HOST + API.DUMP_BOUNDARY;
        JsonObjectRequest request = new JsonObjectRequest(Request.Method.GET, url, null,
                response -> {
                    Log.i("Map Fragment", "Dump boundary downloaded");

                    KmlDocument kmlDocument = new KmlDocument();
                    kmlDocument.parseGeoJSON(response.toString());
                    Drawable defaultMarker = AppCompatResources.getDrawable(getContext(), R.drawable.point);
                    Bitmap defaultBitmap = ((BitmapDrawable) defaultMarker).getBitmap();

                    //Bitmap defaultBitmap = BitmapFactory.decodeResource(getResources(), R.drawable.point);

                    Style defaultStyle = new Style(defaultBitmap, 0x00000000, 1f, 0xFFFFFFFF);
                    FolderOverlay overlay = (FolderOverlay) kmlDocument.mKmlRoot.buildOverlay(map, defaultStyle, null, kmlDocument);
                    map.getOverlays().add(overlay);

                    dataManager.saveData("MAP_DUMP", response.toString());

                    mProgress.hide();
                }, error -> {
            if (error instanceof TimeoutError) {
                Log.i("Map Fragment", "onErrorResponse: Timeout");
                Toast.makeText(getContext(), "Time out", Toast.LENGTH_LONG).show();
            } else if (error instanceof ServerError) {
                Log.i("Map Fragment", "onErrorResponse: Server error");
                Toast.makeText(getContext(), "Server error", Toast.LENGTH_LONG).show();
            } else if (error instanceof NetworkError) {
                Log.i("Map Fragment", "onErrorResponse: Network error");
                Toast.makeText(getContext(), "Network error", Toast.LENGTH_LONG).show();
            } else if (error instanceof ParseError) {
                Log.i("Map Fragment", "onErrorResponse: Parse error");
                Toast.makeText(getContext(), "Parse error", Toast.LENGTH_LONG).show();
            } else {
                Log.i("Map Fragment", "onErrorResponse: Something went wrong ");
                Toast.makeText(getContext(), "Other error", Toast.LENGTH_LONG).show();
            }
        });
        request.setRetryPolicy(new DefaultRetryPolicy(15000, DefaultRetryPolicy.DEFAULT_MAX_RETRIES, DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));
        request.setShouldCache(false);
        mQueue.add(request);
    }

    private void loadCachedOverlay() {
        String blockData = dataManager.getData("MAP_BLOCK");
        String dumpData = dataManager.getData("MAP_DUMP");

        KmlDocument overlayBlock = new KmlDocument();
        KmlDocument overlayDump = new KmlDocument();

        overlayBlock.parseGeoJSON(blockData);
        overlayDump.parseGeoJSON(dumpData);

        Drawable defaultMarker = AppCompatResources.getDrawable(getContext(), R.drawable.point);
        Bitmap defaultBitmap = ((BitmapDrawable) defaultMarker).getBitmap();
        //Bitmap defaultBitmap = BitmapFactory.decodeResource(getResources(), R.drawable.point);

        Style blockStyle = new Style(null, 0x901010AA, 5f, 0x20AA1010);
        Style dumpStyle = new Style(defaultBitmap, 0x00000000, 1f, 0xFFFFFFFF);

        FolderOverlay block = (FolderOverlay) overlayBlock.mKmlRoot.buildOverlay(map, blockStyle, null, overlayBlock);
        FolderOverlay dump = (FolderOverlay) overlayDump.mKmlRoot.buildOverlay(map, dumpStyle, null, overlayDump);

        map.getOverlays().add(block);
        map.getOverlays().add(dump);

        mProgress.hide();
    }
}
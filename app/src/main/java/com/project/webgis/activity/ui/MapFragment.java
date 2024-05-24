package com.project.webgis.activity.ui;

import android.app.ProgressDialog;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Bundle;
import android.os.Handler;
import android.preference.PreferenceManager;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AlertDialog;
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
import com.google.android.material.bottomsheet.BottomSheetDialog;
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
    private CheckBox block, hgu, afdeling, planted, road, bridge, patok, dump;
    private boolean chkBlock, chkHgu, chkAfdeling, chkPlanted, chkRoad, chkBridge, chkPatok, chkDump;
    private FolderOverlay ovlBlock, ovlHgu, ovlAfdeling, ovlPlanted, ovlRoad, ovlBridge, ovlPatok, ovlDump;

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

        chkBlock = false;
        chkHgu = false;
        chkAfdeling = false;
        chkPlanted = false;
        chkRoad = false;
        chkBridge = false;
        chkPatok = false;
        chkDump = false;

        layerButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                BottomSheetDialog dialog = new BottomSheetDialog(getContext());
                View view = getLayoutInflater().inflate(R.layout.bottom_sheet_dialog, null);
                Button btnClose = view.findViewById(R.id.idBtnDismiss);

                block = view.findViewById(R.id.chkBlock);
                hgu = view.findViewById(R.id.chkHgu);
                afdeling = view.findViewById(R.id.chkAfdeling);
                planted = view.findViewById(R.id.chkPlanted);
                road = view.findViewById(R.id.chkRoad);
                bridge = view.findViewById(R.id.chkBridge);
                patok = view.findViewById(R.id.chkPatok);
                dump = view.findViewById(R.id.chkDump);

                block.setChecked(chkBlock);
                hgu.setChecked(chkHgu);
                afdeling.setChecked(chkAfdeling);
                planted.setChecked(chkPlanted);
                road.setChecked(chkRoad);
                bridge.setChecked(chkBridge);
                patok.setChecked(chkPatok);
                dump.setChecked(chkDump);

                block.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        if (block.isChecked()) {
                            map.getOverlays().add(ovlBlock);
                            chkBlock = true;
                        } else {
                            map.getOverlays().remove(ovlBlock);
                            chkBlock = false;
                        }

                    }
                });

                hgu.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        if (hgu.isChecked()) {
                            map.getOverlays().add(ovlHgu);
                            chkHgu = true;
                        } else {
                            map.getOverlays().remove(ovlHgu);
                            chkHgu = false;
                        }
                    }
                });

                afdeling.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        if (afdeling.isChecked()) {
                            map.getOverlays().add(ovlAfdeling);
                            chkAfdeling = true;
                        } else {
                            map.getOverlays().remove(ovlAfdeling);
                            chkAfdeling = false;
                        }
                    }
                });

                planted.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        if (planted.isChecked()) {
                            //map.getOverlays().add(ovlPlanted);
                            chkPlanted = true;
                        } else {
                            //map.getOverlays().remove(ovlPlanted);
                            chkPlanted = false;
                        }

                    }
                });

                road.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        if (road.isChecked()) {
                            //map.getOverlays().add(ovlRoad);
                            chkRoad = true;
                        } else {
                            //map.getOverlays().remove(ovlRoad);
                            chkRoad = false;
                        }

                    }
                });

                bridge.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        if (bridge.isChecked()) {
                            map.getOverlays().add(ovlBridge);
                            chkBridge = true;
                        } else {
                            map.getOverlays().remove(ovlBridge);
                            chkBridge = false;
                        }

                    }
                });

                patok.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        if (patok.isChecked()) {
                            map.getOverlays().add(ovlPatok);
                            chkPatok = true;
                        } else {
                            map.getOverlays().remove(ovlPatok);
                            chkPatok = false;
                        }

                    }
                });

                dump.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        if (dump.isChecked()) {
                            map.getOverlays().add(ovlDump);
                            chkDump = true;
                        } else {
                            map.getOverlays().remove(ovlDump);
                            chkDump = false;
                        }

                    }
                });

                btnClose.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        dialog.dismiss();
                    }
                });

                dialog.setCancelable(false);
                dialog.setContentView(view);
                dialog.show();

            }
        });

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
            if (dataManager.isDataAvailable("MAP_BLOCK") &&
                    dataManager.isDataAvailable("MAP_HGU") &&
                    dataManager.isDataAvailable("MAP_AFDELING") &&
                    dataManager.isDataAvailable("MAP_BRIDGE") &&
                    dataManager.isDataAvailable("MAP_PATOK") &&
                    dataManager.isDataAvailable("MAP_DUMP")) {
                if (isOnline()) {
                    loadMap();
                } else {
                    loadCachedMap();
                }
            } else {
                if (isOnline()) {
                    loadMap();
                } else {
                    networkUnavailable();
                }
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

    private void loadMap() {
        Log.i("Map Fragment", "Downloading block boundary");
        String urlBlock = HOST + API.BLOCK_BOUNDARY;
        JsonObjectRequest requestBlock = new JsonObjectRequest(Request.Method.GET, urlBlock, null,
                response -> {
                    Log.i("Map Fragment", "Block boundary downloaded");

                    KmlDocument kmlDocument = new KmlDocument();
                    kmlDocument.parseGeoJSON(response.toString());
                    Style defaultStyle = new Style(null, 0xB4000000, 5f, 0x64AA1010);
                    ovlBlock = (FolderOverlay) kmlDocument.mKmlRoot.buildOverlay(map, defaultStyle, null, kmlDocument);

                    dataManager.saveData("MAP_BLOCK", response.toString());

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
        requestBlock.setRetryPolicy(new DefaultRetryPolicy(15000, DefaultRetryPolicy.DEFAULT_MAX_RETRIES, DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));
        requestBlock.setShouldCache(false);
        mQueue.add(requestBlock);

        Log.i("Map Fragment", "Downloading hgu boundary");
        String urlHgu = HOST + API.HGU_BOUNDARY;
        JsonObjectRequest requestHgu = new JsonObjectRequest(Request.Method.GET, urlHgu, null,
                response -> {
                    Log.i("Map Fragment", "Hgu boundary downloaded");

                    KmlDocument kmlDocument = new KmlDocument();
                    kmlDocument.parseGeoJSON(response.toString());
                    Style defaultStyle = new Style(null, 0xFFFF0000, 5f, 0x00000000);
                    ovlHgu = (FolderOverlay) kmlDocument.mKmlRoot.buildOverlay(map, defaultStyle, null, kmlDocument);

                    dataManager.saveData("MAP_HGU", response.toString());
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
        requestHgu.setRetryPolicy(new DefaultRetryPolicy(15000, DefaultRetryPolicy.DEFAULT_MAX_RETRIES, DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));
        requestHgu.setShouldCache(false);
        mQueue.add(requestHgu);

        Log.i("Map Fragment", "Downloading afdeling boundary");
        String urlAfdeling = HOST + API.AFDELING_BOUNDARY;
        JsonObjectRequest requestAfdeling = new JsonObjectRequest(Request.Method.GET, urlAfdeling, null,
                response -> {
                    Log.i("Map Fragment", "Afdeling boundary downloaded");

                    KmlDocument kmlDocument = new KmlDocument();
                    kmlDocument.parseGeoJSON(response.toString());
                    Style defaultStyle = new Style(null, 0xB4000000, 5f, 0x644C9900);
                    ovlAfdeling = (FolderOverlay) kmlDocument.mKmlRoot.buildOverlay(map, defaultStyle, null, kmlDocument);

                    dataManager.saveData("MAP_AFDELING", response.toString());
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
        requestAfdeling.setRetryPolicy(new DefaultRetryPolicy(15000, DefaultRetryPolicy.DEFAULT_MAX_RETRIES, DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));
        requestAfdeling.setShouldCache(false);
        mQueue.add(requestAfdeling);

        Log.i("Map Fragment", "Downloading bridge boundary");
        String urlBridge = HOST + API.BRIDGE_BOUNDARY;
        JsonObjectRequest requestBridge = new JsonObjectRequest(Request.Method.GET, urlBridge, null,
                response -> {
                    Log.i("Map Fragment", "Bridge boundary downloaded");

                    KmlDocument kmlDocument = new KmlDocument();
                    kmlDocument.parseGeoJSON(response.toString());
                    Drawable defaultMarker = AppCompatResources.getDrawable(getContext(), R.drawable.point_yellow);
                    Bitmap defaultBitmap = ((BitmapDrawable) defaultMarker).getBitmap();
                    Style defaultStyle = new Style(defaultBitmap, 0xB4000000, 5f, 0x64CCCC00);
                    ovlBridge = (FolderOverlay) kmlDocument.mKmlRoot.buildOverlay(map, defaultStyle, null, kmlDocument);

                    dataManager.saveData("MAP_BRIDGE", response.toString());
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
        requestBridge.setRetryPolicy(new DefaultRetryPolicy(15000, DefaultRetryPolicy.DEFAULT_MAX_RETRIES, DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));
        requestBridge.setShouldCache(false);
        mQueue.add(requestBridge);

        Log.i("Map Fragment", "Downloading patok boundary");
        String urlPatok = HOST + API.PATOK_BOUNDARY;
        JsonObjectRequest requestPatok = new JsonObjectRequest(Request.Method.GET, urlPatok, null,
                response -> {
                    Log.i("Map Fragment", "Patok boundary downloaded");

                    KmlDocument kmlDocument = new KmlDocument();
                    kmlDocument.parseGeoJSON(response.toString());
                    Drawable defaultMarker = AppCompatResources.getDrawable(getContext(), R.drawable.point_red);
                    Bitmap defaultBitmap = ((BitmapDrawable) defaultMarker).getBitmap();
                    Style defaultStyle = new Style(defaultBitmap, 0xB4000000, 5f, 0x64CCCC00);
                    ovlPatok = (FolderOverlay) kmlDocument.mKmlRoot.buildOverlay(map, defaultStyle, null, kmlDocument);

                    dataManager.saveData("MAP_PATOK", response.toString());
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
        requestPatok.setRetryPolicy(new DefaultRetryPolicy(15000, DefaultRetryPolicy.DEFAULT_MAX_RETRIES, DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));
        requestPatok.setShouldCache(false);
        mQueue.add(requestPatok);

        Log.i("Map Fragment", "Downloading dump boundary");
        String urlDump = HOST + API.DUMP_BOUNDARY;
        JsonObjectRequest requestDump = new JsonObjectRequest(Request.Method.GET, urlDump, null,
                response -> {
                    Log.i("Map Fragment", "Dump boundary downloaded");

                    KmlDocument kmlDocument = new KmlDocument();
                    kmlDocument.parseGeoJSON(response.toString());
                    Drawable defaultMarker = AppCompatResources.getDrawable(getContext(), R.drawable.point_white);
                    Bitmap defaultBitmap = ((BitmapDrawable) defaultMarker).getBitmap();
                    Style defaultStyle = new Style(defaultBitmap, 0xB4000000, 5f, 0x64CCCC00);
                    ovlDump = (FolderOverlay) kmlDocument.mKmlRoot.buildOverlay(map, defaultStyle, null, kmlDocument);

                    dataManager.saveData("MAP_DUMP", response.toString());
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
        requestDump.setRetryPolicy(new DefaultRetryPolicy(15000, DefaultRetryPolicy.DEFAULT_MAX_RETRIES, DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));
        requestDump.setShouldCache(false);
        mQueue.add(requestDump);
    }

    private void loadCachedMap() {
        String blockData = dataManager.getData("MAP_BLOCK");
        String hguData = dataManager.getData("MAP_HGU");
        String afdelingData = dataManager.getData("MAP_AFDELING");
        String bridgeData = dataManager.getData("MAP_BRIDGE");
        String patokData = dataManager.getData("MAP_PATOK");
        String dumpData = dataManager.getData("MAP_DUMP");

        KmlDocument kmlBlock = new KmlDocument();
        KmlDocument kmlHgu = new KmlDocument();
        KmlDocument kmlAfdeling = new KmlDocument();
        KmlDocument kmlBridge = new KmlDocument();
        KmlDocument kmlPatok = new KmlDocument();
        KmlDocument kmlDump = new KmlDocument();

        kmlBlock.parseGeoJSON(blockData);
        kmlHgu.parseGeoJSON(hguData);
        kmlAfdeling.parseGeoJSON(afdelingData);
        kmlBridge.parseGeoJSON(bridgeData);
        kmlPatok.parseGeoJSON(patokData);
        kmlDump.parseGeoJSON(dumpData);

        Drawable bridgeMarker = AppCompatResources.getDrawable(getContext(), R.drawable.point_yellow);
        Bitmap bridgeBitmap = ((BitmapDrawable) bridgeMarker).getBitmap();

        Drawable patokMarker = AppCompatResources.getDrawable(getContext(), R.drawable.point_red);
        Bitmap patokBitmap = ((BitmapDrawable) patokMarker).getBitmap();

        Drawable dumpMarker = AppCompatResources.getDrawable(getContext(), R.drawable.point_white);
        Bitmap dumpBitmap = ((BitmapDrawable) dumpMarker).getBitmap();

        Style blockStyle = new Style(null, 0xB4000000, 5f, 0x64AA1010);
        ovlBlock = (FolderOverlay) kmlBlock.mKmlRoot.buildOverlay(map, blockStyle, null, kmlBlock);

        Style hguStyle = new Style(null, 0xFFFF0000, 5f, 0x00000000);
        ovlHgu = (FolderOverlay) kmlHgu.mKmlRoot.buildOverlay(map, hguStyle, null, kmlHgu);

        Style afdelingStyle = new Style(null, 0xB4000000, 5f, 0x644C9900);
        ovlAfdeling = (FolderOverlay) kmlAfdeling.mKmlRoot.buildOverlay(map, afdelingStyle, null, kmlAfdeling);

        Style bridgeStyle = new Style(bridgeBitmap, 0xB4000000, 5f, 0x64CCCC00);
        ovlBridge = (FolderOverlay) kmlBridge.mKmlRoot.buildOverlay(map, bridgeStyle, null, kmlBridge);

        Style patokStyle = new Style(patokBitmap, 0xB4000000, 5f, 0x64CCCC00);
        ovlPatok = (FolderOverlay) kmlPatok.mKmlRoot.buildOverlay(map, patokStyle, null, kmlPatok);

        Style dumpStyle = new Style(dumpBitmap, 0xB4000000, 5f, 0x64CCCC00);
        ovlDump = (FolderOverlay) kmlDump.mKmlRoot.buildOverlay(map, dumpStyle, null, kmlDump);

        mProgress.hide();
    }

    public boolean isOnline() {
        ConnectivityManager cm = (ConnectivityManager) getContext().getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo netInfo = cm.getActiveNetworkInfo();
        return netInfo != null && netInfo.isConnectedOrConnecting();
    }

    private void networkUnavailable() {
        AlertDialog.Builder builder = new AlertDialog.Builder(getContext());
        builder.setTitle("Network unavailable");
        builder.setMessage("Please connect to internet to loading data");
        builder.show();
    }
}
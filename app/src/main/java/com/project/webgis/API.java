package com.project.webgis;

public interface API {
    String LOGIN_URL = "/api/v1/account/loginRequest";


    /**
     * Data Urls
     */
    String PATOK_TABLE = "/api/v1/data/patok";
    String PLANTED_TABLE = "/api/v1/data/planted";
    String DUMP_TABLE = "/api/v1/data/dump";
    String APL_TABLE = "/api/v1/data/apl";
    String DUMP_SAVE = "/api/v1/save/dump/";
    String PATOK_SAVE = "/api/v1/save/patok/";
    String TANKOS_CHART = "/api/v1/tankos/chart";

    /**
     * Map Urls
     */
    String BLOCK_BOUNDARY = "/api/v1/map/block";
    String HGU_BOUNDARY = "/api/v1/map/hgu";
    String AFDELING_BOUNDARY = "/api/v1/map/afdeling";
    String PLANTED_BOUNDARY = "/api/v1/map/planted";
    String ROAD_BOUNDARY = "/api/v1/map/road";
    String BRIDGE_BOUNDARY = "/api/v1/map/bridge";
    String PATOK_BOUNDARY = "/api/v1/map/patok";
    String DUMP_BOUNDARY = "/api/v1/map/dump";
}

package com.project.webgis;

public interface API {
    String LOGIN_URL = "/api/v1/account/loginRequest";


    /**
     * Data Urls
     */
    String PATOK_TABLE = "/api/v1/data/patok";
    String PLANTED_TABLE = "/api/v1/data/planted";
    String DUMP_TABLE = "/api/v1/data/dump";
    String DUMP_SAVE = "/api/v1/save/dump/";

    /**
     * Map Urls
     */
    String BLOCK_BOUNDARY = "/api/v1/map/block";
    String DUMP_BOUNDARY = "/api/v1/map/dump";
}

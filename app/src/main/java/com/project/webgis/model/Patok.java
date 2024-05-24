package com.project.webgis.model;

public class Patok {
    int id;
    String no;
    String afdeling;
    String block;
    String latitude;
    String longtitude;
    String period;
    String status;

    public Patok() {

    }

    public Patok(int id, String no, String afdeling, String block, String latitude, String longtitude, String period, String status) {
        this.id = id;
        this.no = no;
        this.afdeling = afdeling;
        this.block = block;
        this.latitude = latitude;
        this.longtitude = longtitude;
        this.period = period;
        this.status = status;
    }

    public int getId() {
        return id;
    }

    public String getNo() {
        return no;
    }

    public String getAfdeling() {
        return afdeling;
    }

    public String getBlock() {
        return block;
    }

    public String getLatitude() {
        return latitude;
    }

    public String getLongtitude() {
        return longtitude;
    }

    public String getPeriod() {
        return period;
    }

    public String getStatus() {
        return status;
    }
}

package com.project.webgis.model;

public class Tankos {
    int id;
    String afdeling;
    String block;
    String location;
    String dump_date;

    public Tankos() {

    }

    public Tankos(int id, String afdeling, String block, String location, String dump_date) {
        this.id = id;
        this.afdeling = afdeling;
        this.block = block;
        this.location = location;
        this.dump_date = dump_date;
    }

    public int getId() {
        return id;
    }

    public String getAfdeling() {
        return afdeling;
    }

    public String getBlock() {
        return block;
    }

    public String getLocation() {
        return location;
    }

    public String getDump_date() {
        return dump_date;
    }
}

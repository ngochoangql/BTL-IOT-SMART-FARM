package com.example.smartfarm;

import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.lang.reflect.Type;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Timer;
import java.util.TimerTask;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class MainActivity extends AppCompatActivity {

    MqttHelper mqttHelper;
    List<Scheduler> schedulers = new ArrayList<>();
    LinearLayout list ;
    OkHttpClient client = new OkHttpClient();
    Timer timer;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);
        timer = new Timer();
        mqttHelper = new MqttHelper("smart-app",this);
        timer.schedule(new TimerTask() {
            @Override
            public void run() {
                String url = "http://192.168.1.7:3000/api/schedulers";

                Request request = new Request.Builder()
                        .url(url)
                        .build();

                try {
                    Response response = client.newCall(request).execute();
                    if (response.isSuccessful()) {
                        String json = response.body().string();

                        json = json.replace("'", "\"");
                        Gson gson = new Gson();
                        Type schedulerListType = new TypeToken<List<Scheduler>>(){}.getType();
                        schedulers = gson.fromJson(json, schedulerListType);

                        Log.d("hoang",schedulers.toString());
                        update();
                    } else {
                        // Xử lý lỗi nếu có
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                    // Xử lý lỗi kết nối
                }
            }
        },0);


        list = findViewById(R.id.schedulers);

        Button add = findViewById(R.id.button2);
        add.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, AddSchedule.class);
                startActivity(intent);
            }
        });
    }

    public void update(){
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                for (Scheduler scheduler : schedulers){
                    View view = getLayoutInflater().inflate(R.layout.schedule,null,false);

                    TextView nameS = view.findViewById(R.id.nameS);
                    TextView cycleS = view.findViewById(R.id.cycleS);
                    TextView flow1S = view.findViewById(R.id.flow1S);
                    TextView flow2S = view.findViewById(R.id.flow2S);
                    TextView flow3S = view.findViewById(R.id.flow3S);
                    TextView startTS = view.findViewById(R.id.startTS);
                    TextView stopTS = view.findViewById(R.id.stopTS);
                    Button onOff = view.findViewById(R.id.onOff);
                    if (scheduler.isActive){
                        onOff.setText("On");
                        onOff.setBackgroundColor(0xFF059212);
                    }else{
                        onOff.setText("Off");
                        onOff.setBackgroundColor(0xFFE72929);
                    }
                    onOff.setOnClickListener(new View.OnClickListener() {
                        @Override
                        public void onClick(View v) {
                            if (onOff.getText().equals("On")){
                                onOff.setText("Off");
                                onOff.setBackgroundColor(0xFFE72929);
                                mqttHelper.publish("update-schedule","{\"id\":\""+scheduler.id+"\",\"isActive\":false}",0,false);
                            }else{
                                onOff.setText("On");
                                onOff.setBackgroundColor(0xFF059212);
                                mqttHelper.publish("update-schedule","{\"id\":\""+scheduler.id+"\",\"isActive\":true}",0,false);
                            }
                        }
                    });
                    nameS.setText("Scheduler Name :" + scheduler.schedulerName);
                    cycleS.setText("Cycle :" +Integer.toString(scheduler.cycle));
                    flow1S.setText("Flow1 :" +Integer.toString(scheduler.flow1));
                    flow2S.setText("Flow1 :" +Integer.toString(scheduler.flow1));
                    flow3S.setText("Flow1 :" +Integer.toString(scheduler.flow1));
                    startTS.setText("Start Time :" +scheduler.startTime);
                    stopTS.setText("Stop Time :" +scheduler.stopTime);
                    list.addView(view);

                }
            }
        });

    }
}
package com.codsoft.quoteoftheday;

import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import java.util.ArrayList;
import java.util.List;

public class FavoritesActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_favorites);

        ListView listView = findViewById(R.id.lvFavorites);
        TextView tvEmpty = findViewById(R.id.tvEmpty);

        List<String[]> favorites = MainActivity.favoritesList;

        if (favorites.isEmpty()) {
            tvEmpty.setVisibility(android.view.View.VISIBLE);
            listView.setVisibility(android.view.View.GONE);
        } else {
            tvEmpty.setVisibility(android.view.View.GONE);
            listView.setVisibility(android.view.View.VISIBLE);

            List<String> displayList = new ArrayList<>();
            for (String[] fav : favorites) {
                displayList.add('"' + fav[0] + '"' + "\n— " + fav[1]);
            }

            ArrayAdapter<String> adapter = new ArrayAdapter<>(
                    this,
                    android.R.layout.simple_list_item_1,
                    displayList
            );
            listView.setAdapter(adapter);
        }
    }
}

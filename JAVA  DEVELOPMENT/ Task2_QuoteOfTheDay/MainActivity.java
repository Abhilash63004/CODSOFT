package com.codsoft.quoteoftheday;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class MainActivity extends AppCompatActivity {

    private TextView tvQuote, tvAuthor;
    private ImageButton btnFavorite;
    private Button btnShare, btnNewQuote, btnViewFavorites;

    private final String[][] quotes = {
        {"The only way to do great work is to love what you do.", "Steve Jobs"},
        {"In the middle of every difficulty lies opportunity.", "Albert Einstein"},
        {"It does not matter how slowly you go as long as you do not stop.", "Confucius"},
        {"Life is what happens when you're busy making other plans.", "John Lennon"},
        {"Strive not to be a success, but rather to be of value.", "Albert Einstein"},
        {"You miss 100% of the shots you don't take.", "Wayne Gretzky"},
        {"The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"},
        {"It is during our darkest moments that we must focus to see the light.", "Aristotle"},
        {"Spread love everywhere you go.", "Mother Teresa"},
        {"Believe you can and you're halfway there.", "Theodore Roosevelt"},
        {"Act as if what you do makes a difference. It does.", "William James"},
        {"Success is not final, failure is not fatal: it is the courage to continue that counts.", "Winston Churchill"},
    };

    // Stored favorites (in-memory; use SharedPreferences or Room DB for persistence)
    public static List<String[]> favoritesList = new ArrayList<>();

    private int currentIndex = 0;
    private boolean isFavorite = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        tvQuote = findViewById(R.id.tvQuote);
        tvAuthor = findViewById(R.id.tvAuthor);
        btnFavorite = findViewById(R.id.btnFavorite);
        btnShare = findViewById(R.id.btnShare);
        btnNewQuote = findViewById(R.id.btnNewQuote);
        btnViewFavorites = findViewById(R.id.btnViewFavorites);

        // Show a random quote on launch
        showRandomQuote();

        btnNewQuote.setOnClickListener(v -> showRandomQuote());

        btnFavorite.setOnClickListener(v -> toggleFavorite());

        btnShare.setOnClickListener(v -> shareQuote());

        btnViewFavorites.setOnClickListener(v -> {
            Intent intent = new Intent(MainActivity.this, FavoritesActivity.class);
            startActivity(intent);
        });
    }

    private void showRandomQuote() {
        Random random = new Random();
        currentIndex = random.nextInt(quotes.length);
        tvQuote.setText('"' + quotes[currentIndex][0] + '"');
        tvAuthor.setText("— " + quotes[currentIndex][1]);

        // Check if already in favorites
        isFavorite = isAlreadyFavorite();
        updateFavoriteIcon();
    }

    private boolean isAlreadyFavorite() {
        String currentQuote = quotes[currentIndex][0];
        for (String[] fav : favoritesList) {
            if (fav[0].equals(currentQuote)) return true;
        }
        return false;
    }

    private void toggleFavorite() {
        if (isFavorite) {
            // Remove from favorites
            favoritesList.removeIf(fav -> fav[0].equals(quotes[currentIndex][0]));
            isFavorite = false;
            Toast.makeText(this, "Removed from favorites", Toast.LENGTH_SHORT).show();
        } else {
            // Add to favorites
            favoritesList.add(quotes[currentIndex]);
            isFavorite = true;
            Toast.makeText(this, "Added to favorites!", Toast.LENGTH_SHORT).show();
        }
        updateFavoriteIcon();
    }

    private void updateFavoriteIcon() {
        if (isFavorite) {
            btnFavorite.setImageResource(android.R.drawable.btn_star_big_on);
        } else {
            btnFavorite.setImageResource(android.R.drawable.btn_star_big_off);
        }
    }

    private void shareQuote() {
        String shareText = '"' + quotes[currentIndex][0] + '"' + "\n— " + quotes[currentIndex][1];
        Intent intent = new Intent(Intent.ACTION_SEND);
        intent.setType("text/plain");
        intent.putExtra(Intent.EXTRA_TEXT, shareText);
        startActivity(Intent.createChooser(intent, "Share Quote via"));
    }
}

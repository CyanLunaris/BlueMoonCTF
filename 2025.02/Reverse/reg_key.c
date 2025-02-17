#include <gtk/gtk.h>
#include <string.h>

GtkWidget *window;
GtkWidget *entry;
GtkWidget *label;

const char expected_key[] = "4d3v3L0p3R2024@c0D3";
const char flag[] = "school21[r3v3rs3_3ng1n33r1ng]";

static void check_key(GtkWidget *widget, gpointer data) {
    const char *input = gtk_entry_get_text(GTK_ENTRY(entry));
    
    if (strlen(input) != strlen(expected_key)) {
        gtk_label_set_text(GTK_LABEL(label), "Неверный ключ!");
        return;
    }
    
    // Простая проверка ключа
    int valid = 1;
    for (int i = 0; i < strlen(expected_key); i++) {
        if (input[i] != expected_key[i]) {
            valid = 0;
            break;
        }
    }
    
    if (valid) {
        gtk_label_set_text(GTK_LABEL(label), flag);
    } else {
        gtk_label_set_text(GTK_LABEL(label), "Неверный ключ!");
    }
}

int main(int argc, char *argv[]) {
    gtk_init(&argc, &argv);
    
    // Создание окна
    window = gtk_window_new(GTK_WINDOW_TOPLEVEL);
    gtk_window_set_title(GTK_WINDOW(window), "Регистрация");
    gtk_container_set_border_width(GTK_CONTAINER(window), 10);
    gtk_window_set_default_size(GTK_WINDOW(window), 300, 150);
    g_signal_connect(window, "destroy", G_CALLBACK(gtk_main_quit), NULL);
    
    // Создание вертикального контейнера
    GtkWidget *vbox = gtk_box_new(GTK_ORIENTATION_VERTICAL, 5);
    gtk_container_add(GTK_CONTAINER(window), vbox);
    
    // Добавление поля ввода
    entry = gtk_entry_new();
    gtk_box_pack_start(GTK_BOX(vbox), entry, TRUE, TRUE, 0);
    
    // Добавление кнопки
    GtkWidget *button = gtk_button_new_with_label("Проверить ключ");
    g_signal_connect(button, "clicked", G_CALLBACK(check_key), NULL);
    gtk_box_pack_start(GTK_BOX(vbox), button, TRUE, TRUE, 0);
    
    // Добавление метки для результата
    label = gtk_label_new("");
    gtk_box_pack_start(GTK_BOX(vbox), label, TRUE, TRUE, 0);
    
    gtk_widget_show_all(window);
    gtk_main();
    
    return 0;
}
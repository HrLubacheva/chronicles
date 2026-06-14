import os
from pathlib import Path
from datetime import datetime


def merge_all_md_files_recursive(source_dir, output_file='all_md_merged.md'):
    """
    Рекурсивно обходит ВСЕ папки и подпапки, собирает только .md файлы в один.
    Пропускает виртуальные окружения и другие ненужные папки.
    Оригиналы НЕ УДАЛЯЮТСЯ.
    """
    source_path = Path(source_dir)

    if not source_path.exists():
        print(f"❌ Ошибка: Папка '{source_dir}' не найдена!")
        return

    # Папки для пропуска
    skip_folders = {'.venv', 'venv', 'env', '.env', '__pycache__', '.git', '.idea', 'node_modules', 'dist', 'build'}

    # Собираем все .md файлы, пропуская ненужные папки
    md_files = []

    print(f"🔍 Поиск .md файлов в: {source_path.absolute()}")
    print(f"🚫 Игнорируем папки: {', '.join(skip_folders)}")
    print()

    for root, dirs, files in os.walk(source_path):
        # Удаляем из обхода папки, которые нужно пропустить
        dirs[:] = [d for d in dirs if d not in skip_folders]

        # Добавляем только .md файлы
        for file in files:
            if file.endswith('.md'):
                full_path = Path(root) / file
                md_files.append(full_path)

    # Сортируем для консистентного порядка
    md_files.sort()

    if not md_files:
        print(f"⚠️  В папке '{source_dir}' и её подпапках не найдено .md файлов!")
        return

    print(f"📄 Найдено .md файлов: {len(md_files)}")

    # Показываем пример найденных файлов
    print("\n📁 Найденные файлы (первые 10):")
    for f in md_files[:10]:
        try:
            rel_path = f.relative_to(source_path)
            print(f"  - {rel_path}")
        except:
            print(f"  - {f}")
    if len(md_files) > 10:
        print(f"  ... и ещё {len(md_files) - 10} файлов")

    total_size = 0
    files_by_folder = {}

    print(f"\n📝 Начинаем объединение в файл: {output_file}")
    print("=" * 60)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Заголовок с информацией
        outfile.write(f"# ОБЪЕДИНЕНИЕ ВСЕХ MD ФАЙЛОВ\n\n")
        outfile.write(f"**Дата создания:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        outfile.write(f"**Источник:** {source_path.absolute()}\n")
        outfile.write(f"**Всего найдено файлов:** {len(md_files)}\n")
        outfile.write(f"**Этот файл содержит копии всех .md файлов из всех подпапок.**\n")
        outfile.write(f"**Оригиналы сохранены и не изменены.**\n\n")
        outfile.write("---\n\n")

        for i, md_file in enumerate(md_files, 1):
            try:
                # Получаем относительный путь
                try:
                    rel_path = md_file.relative_to(source_path)
                except:
                    rel_path = md_file.name

                # Определяем папку
                folder_name = rel_path.parent if rel_path.parent != Path('.') else 'корневая_папка'
                folder_key = str(folder_name)
                files_by_folder[folder_key] = files_by_folder.get(folder_key, 0) + 1

                # Читаем содержимое файла
                with open(md_file, 'r', encoding='utf-8') as infile:
                    content = infile.read()
                    total_size += len(content.encode('utf-8'))

                # Записываем разделитель с информацией
                outfile.write(f"\n\n{'=' * 80}\n")
                outfile.write(f"ФАЙЛ: {rel_path}\n")
                outfile.write(f"ПАПКА: {folder_name}\n")
                outfile.write(f"#{i} из {len(md_files)}\n")
                outfile.write(f"{'=' * 80}\n\n")

                # Записываем содержимое
                outfile.write(content)
                outfile.write(f"\n\n{'─' * 80}\n")

                # Прогресс каждые 50 файлов
                if i % 50 == 0 or i == len(md_files):
                    print(f"  📊 Прогресс: {i}/{len(md_files)} файлов ({i / len(md_files) * 100:.1f}%)")

            except Exception as e:
                print(f"  ❌ Ошибка в файле {md_file.name}: {e}")

        # Финальная статистика
        outfile.write(f"\n\n{'#' * 80}\n")
        outfile.write("# СТАТИСТИКА ОБЪЕДИНЕНИЯ\n")
        outfile.write(f"{'#' * 80}\n\n")
        outfile.write(f"**Всего файлов:** {len(md_files)}\n")
        outfile.write(f"**Общий размер:** {total_size / 1024:.2f} KB ({total_size / 1024 / 1024:.2f} MB)\n\n")

        outfile.write("**Распределение по папкам:**\n")
        for folder, count in sorted(files_by_folder.items()):
            outfile.write(f"- `{folder}`: {count} файлов\n")

    # Вывод финальной статистики
    print("\n" + "=" * 60)
    print(f"✅ ОБЪЕДИНЕНИЕ ЗАВЕРШЕНО!")
    print(f"📄 Всего обработано файлов: {len(md_files)}")
    print(f"📊 Общий размер: {total_size / 1024:.2f} KB ({total_size / 1024 / 1024:.2f} MB)")
    print(f"📁 Затронуто папок: {len(files_by_folder)}")
    print(f"💾 Результат сохранён в: {Path(output_file).absolute()}")
    print(f"🔒 Оригинальные файлы остались нетронутыми")

    # Показываем распределение
    print("\n📊 Топ-10 папок по количеству файлов:")
    for folder, count in sorted(files_by_folder.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  - {folder}: {count} файлов")


# ПРОСТАЯ ВЕРСИЯ (без лишних заголовков, только содержимое)
def merge_all_md_files_simple(source_dir, output_file='all_md_simple.md'):
    """
    Простая версия - просто склеивает все .md файлы без лишних заголовков.
    Пропускает .venv и берёт только .md файлы.
    """
    source_path = Path(source_dir)

    if not source_path.exists():
        print(f"❌ Ошибка: Папка '{source_dir}' не найдена!")
        return

    skip_folders = {'.venv', 'venv', 'env', '.env', '__pycache__', '.git', '.idea', 'node_modules'}

    md_files = []
    for root, dirs, files in os.walk(source_path):
        dirs[:] = [d for d in dirs if d not in skip_folders]
        for file in files:
            if file.endswith('.md'):
                md_files.append(Path(root) / file)

    md_files.sort()

    if not md_files:
        print(f"⚠️  Не найдено .md файлов!")
        return

    print(f"🔍 Найдено {len(md_files)} .md файлов")
    print(f"🚫 Пропущены папки: .venv, venv, env, __pycache__, .git и др.")
    print(f"📝 Объединение в {output_file}...")

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for i, md_file in enumerate(md_files, 1):
            try:
                with open(md_file, 'r', encoding='utf-8') as infile:
                    content = infile.read()

                outfile.write(content)

                if i < len(md_files):
                    outfile.write("\n\n")

                if i % 100 == 0:
                    print(f"  Прогресс: {i}/{len(md_files)}")

            except Exception as e:
                print(f"  ❌ Ошибка в {md_file.name}: {e}")

    print(f"✅ Готово! {len(md_files)} .md файлов объединены в {output_file}")


# ОСНОВНОЙ ЗАПУСК
if __name__ == "__main__":
    # Используем текущую папку
    current_dir = Path.cwd()

    print(f"📍 Текущая папка: {current_dir}")
    print("🔄 Будет выполнен рекурсивный обход ВСЕХ подпапок")
    print("🎯 Будут взяты ТОЛЬКО .md файлы")
    print("🚫 Папка .venv будет пропущена")
    print()

    # ВЫБЕРИТЕ ОДИН ИЗ ВАРИАНТОВ:

    # Вариант 1: Подробный (с заголовками и информацией о каждом файле)
    merge_all_md_files_recursive(current_dir, 'all_md_merged_detailed.md')

    # Вариант 2: Простой (просто склеивает содержимое)
    # merge_all_md_files_simple(current_dir, 'all_md_merged_simple.md')
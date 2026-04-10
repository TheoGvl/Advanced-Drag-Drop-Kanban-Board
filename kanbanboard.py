import flet as ft
import random

def main(page: ft.Page):
    # --- App Configuration ---
    page.title = "Pro Kanban Board"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0E0E11" 
    page.padding = ft.Padding.all(40)
    
    # --- Pylance Strict-Mode Bypass ---
    # Helper function to safely cast lists for Flet's strict 'controls' properties
    def cast_controls(items: list) -> list[ft.Control]:
        return items

    # --- Complex Application State ---
    # The global "Database" holding all our tasks
    state = {
        "tasks": {
            "TODO": [
                {"id": "t1", "title": "Design Database Schema", "tag": "Backend", "color": "#FF453A"},
                {"id": "t2", "title": "Setup Flet Boilerplate", "tag": "UI/UX", "color": "#FF9F0A"}
            ],
            "IN PROGRESS": [
                {"id": "t3", "title": "Implement Drag & Drop API", "tag": "Core", "color": "#BF5AF2"}
            ],
            "DONE": [
                {"id": "t4", "title": "Wireframe Approval", "tag": "Planning", "color": "#32ADE6"}
            ]
        }
    }

    # The main container holding the 3 columns
    board_container = ft.Row(
        spacing=20, 
        alignment=ft.MainAxisAlignment.CENTER, 
        vertical_alignment=ft.CrossAxisAlignment.START
    )

    # --- The Core Logic ---
    def build_board():
        # Clear the board completely for React-style state rehydration
        board_container.controls.clear()

        # Iterate through the dictionary to build columns dynamically
        for column_name, task_list in state["tasks"].items():
            
            task_controls = []
            for task in task_list:
                
                # The visual representation of a single task card
                card_visual = ft.Container(
                    content=ft.Column(controls=cast_controls([
                        ft.Container(
                            bgcolor=task["color"], 
                            padding=ft.Padding.symmetric(horizontal=8, vertical=4), 
                            border_radius=ft.BorderRadius.all(10), 
                            content=ft.Text(task["tag"], size=10, weight=ft.FontWeight.BOLD, color="#000000")
                        ),
                        ft.Text(task["title"], size=14, weight=ft.FontWeight.BOLD)
                    ])),
                    width=260,
                    bgcolor="#1C1C1E",
                    padding=ft.Padding.all(15),
                    border_radius=ft.BorderRadius.all(10),
                    border=ft.border.all(1, "#2C2C2E"),
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="#1A000000")
                )

                # Wrap the visual card in a Draggable API component
                draggable_card = ft.Draggable(
                    group="kanban", 
                    content=card_visual,
                    # What the user sees while dragging
                    content_feedback=ft.Container(content=card_visual, opacity=0.7),
                    # Hidden payload containing the memory reference and source column
                    data={"task_data": task, "source_column": column_name}
                )
                task_controls.append(draggable_card)

            # Handler triggered when a user drops a card onto a valid column
            def drag_accept(e):
                dragged_element = page.get_control(e.src_id)
                
                # Pylance safety check: Ensure the element exists
                if not dragged_element:
                    return
                
                task_data = dragged_element.data["task_data"]
                source_col = str(dragged_element.data["source_column"])
                target_col = str(e.control.data) 

                # Only recalculate if the card was moved to a different column
                if source_col != target_col:
                    # Mutate the global state
                    state["tasks"][source_col].remove(task_data)
                    state["tasks"][target_col].append(task_data)
                    
                    # Force a full UI rebuild based on the new state
                    build_board()
                    page.update()

            # The visual representation of the Column itself
            column_visual = ft.Container(
                content=ft.Column(controls=cast_controls([
                    # Dynamic Header: Title and Task Count
                    ft.Row(controls=cast_controls([
                        ft.Text(column_name, size=16, weight=ft.FontWeight.W_900, color="#FFFFFF"),
                        ft.Container(
                            bgcolor="#2C2C2E", padding=ft.Padding.symmetric(horizontal=8, vertical=2), border_radius=ft.BorderRadius.all(10),
                            content=ft.Text(str(len(task_list)), size=12, weight=ft.FontWeight.BOLD, color="#8E8E93")
                        )
                    ]), alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    
                    ft.Container(height=10),
                    # Inject all generated Draggable cards into this column
                    ft.Column(controls=cast_controls(task_controls), spacing=15)
                ])),
                width=300,
                height=500, # Fixed height to define the drop zone area
                bgcolor="#0A0A0A",
                padding=ft.Padding.all(20),
                border_radius=ft.BorderRadius.all(15),
                border=ft.border.all(1, "#1C1C1E")
            )

            # Wrap the column in a DragTarget API to act as a drop zone
            column_target = ft.DragTarget(
                group="kanban",
                content=column_visual,
                data=column_name, # Storing the column name for the drop logic
                on_accept=drag_accept 
            )

            board_container.controls.append(column_target)

    # Initial UI build
    build_board()

    # --- Task Creation Logic ---
    
    # UI Elements for creating a new task
    new_task_input = ft.TextField(
        hint_text="Enter a new task note...", 
        expand=True, 
        bgcolor="#1C1C1E", 
        border_color="#2C2C2E"
    )
    
    tag_dropdown = ft.Dropdown(
        width=150,
        bgcolor="#1C1C1E",
        border_color="#2C2C2E",
        value="UI/UX",
        options=[
            ft.dropdown.Option("UI/UX"),
            ft.dropdown.Option("Backend"),
            ft.dropdown.Option("Core"),
            ft.dropdown.Option("Planning"),
            ft.dropdown.Option("Bugfix")
        ]
    )

    # Function to add the new task to the global state
    def add_new_task(e):
        title = str(new_task_input.value).strip()
        tag = str(tag_dropdown.value)
        
        if not title:
            return # Block empty submissions
            
        # Dictionary mapping tags to specific UI colors
        tag_colors = {
            "UI/UX": "#FF9F0A",
            "Backend": "#FF453A",
            "Core": "#BF5AF2",
            "Planning": "#32ADE6",
            "Bugfix": "#FF375F"
        }
        
        # Create the new payload
        new_task_payload = {
            "id": f"t{random.randint(100, 9999)}", # Random unique ID
            "title": title,
            "tag": tag,
            "color": tag_colors.get(tag, "#FFFFFF")
        }
        
        # Append to the "TODO" array
        state["tasks"]["TODO"].append(new_task_payload)
        
        # Clear the input field
        new_task_input.value = ""
        
        # Rebuild and refresh
        build_board()
        page.update()

    add_btn = ft.ElevatedButton(
        "Add Note",
        icon=ft.Icons.ADD,
        bgcolor="#00D1FF",
        color="#000000",
        on_click=add_new_task
    )

    # The top control panel grouping the inputs
    creation_panel = ft.Container(
        content=ft.Row(controls=cast_controls([
            new_task_input,
            tag_dropdown,
            add_btn
        ])),
        width=940, # Matches the total width of the 3 columns + spacing
        padding=ft.Padding.only(bottom=20)
    )

    # --- Main Page Assembly ---
    header = ft.Row(controls=cast_controls([
        ft.Icon(icon=ft.Icons.VIEW_KANBAN, color="#00D1FF", size=30),
        ft.Text("PROJECT KANBAN", size=24, weight=ft.FontWeight.W_900, color="#FFFFFF")
    ]))

    page.add(
        ft.Column(controls=cast_controls([
            header,
            creation_panel, # Injected the new task creation panel here
            board_container
        ]), horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

ft.run(main)
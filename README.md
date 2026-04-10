# Advanced Drag & Drop Kanban Board

A highly interactive, state-driven project management dashboard built with **Python** and the **Flet** framework. This project moves beyond static UI layouts to demonstrate advanced application state mutation, dynamic re-rendering, data entry handling, and physics-based Drag & Drop interactions.

## 🌟 Key Engineering Features

* **Dynamic Data Entry**: Features a control panel allowing users to create new task notes in real-time. Tasks are automatically injected into the global state dictionary, color-coded based on user-selected dropdown tags, and rendered instantly.
* **Real-time Drag & Drop API**: Utilizes Flet's `ft.Draggable` and `ft.DragTarget` classes to allow users to physically pick up task cards and move them across the screen. Includes visual "ghosting" feedback (`content_feedback`) during the drag event.
* **Complex State Mutation**: When a card is dropped, the `on_accept` event handler captures the memory ID of the dragged element, decodes its payload, mathematically removes the dictionary object from the source array, and appends it to the target array in real-time.
* **React-Style Rehydration**: Employs a component-based architectural pattern (`build_board()` function) that completely clears and dynamically rebuilds the DOM matrix based on the newly mutated global state object, ensuring perfect UI/Data synchronization.
* **100% Strict Type Compliant**: Engineered using explicit type casting (`cast_controls`) and data isolation to bypass strict-mode static checker errors while retaining highly nested layouts. All codebase comments are documented in English.

## Tech Stack

* **Language**: Python 3.8+
* **Framework**: Flet (v0.80.0+)
* **Key Concepts**: Event Handling, Memory Payloads, Data Structure Mutation, Dict/List ops, Real-time DOM Refreshing, Form Validation.

## How to Run

1.  **Install Flet**:
    ```bash
    pip install flet
    ```
2.  **Run the application**:
    ```bash
    python trello_clone.py
    ```

## How to Use

1. **Add a Note:** Type a task description into the top text field, select a category tag from the dropdown, and click "Add Note". Watch it instantly appear in the TODO column.
2. **Move Tasks:** Click and hold any task card. Drag it across the screen.
3. **Drop Tasks:** Release the mouse button while hovering over the "IN PROGRESS" or "DONE" columns.
4. **Observe State Updates:** Watch the application state instantly update: the card snaps into the new column, and the number counters at the top of the columns recalculate mathematically.

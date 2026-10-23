// dynamic interactions and event handling
document.addEventListener("DOMContentLoaded", () => {
    // confirmation modal before deleting articles
    const deleteButtons = document.querySelectorAll(".btn-danger");
    deleteButtons.forEach((button) => {
        button.addEventListener("click", (event) => {
            if (!confirm("Are you sure you want to permanently delete this article?")) {
                event.preventDefault();
            }
        });
    });
});
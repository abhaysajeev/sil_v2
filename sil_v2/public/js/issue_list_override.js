frappe.listview_settings['Issue'] = {
    onload: function (listview) {
        console.log('Issue list JS loaded')
        frappe.after_ajax(() => {
            // Wait for the list to load
            setTimeout(() => {
                const hideStatusColumn = () => {
                    document.querySelectorAll("th[data-fieldname='status'], td[data-fieldname='status']").forEach(el => {
                        el.style.display = "none";
                    });
                };

                // Run once
                hideStatusColumn();

                // Also watch for DOM changes (pagination, filtering, etc.)
                const observer = new MutationObserver(hideStatusColumn);
                const target = document.querySelector(".list-view-container");
                if (target) {
                    observer.observe(target, { childList: true, subtree: true });
                }
            }, 500);  // Add slight delay to ensure DOM is rendered
        });
    }
};

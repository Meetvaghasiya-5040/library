// Book status checking and statistics calculation
      function updateBookStatuses() {
        const today = new Date();
        let onTimeCount = 0;
        let overdueCount = 0;
        let totalPenalty = 0;

        // Get all book elements
        const bookElements = document.querySelectorAll(
          "[data-book-return-date]"
        );

        bookElements.forEach((bookElement) => {
          const returnDateStr = bookElement.getAttribute(
            "data-book-return-date"
          );
          const penaltyStr = bookElement.getAttribute("data-book-penalty");
          const penalty = parseFloat(penaltyStr) || 0;

          totalPenalty += penalty;

          // Parse return date (assuming format YYYY-MM-DD or similar)
          const returnDate = new Date(returnDateStr);
          const timeDiff = returnDate.getTime() - today.getTime();
          const daysDiff = Math.ceil(timeDiff / (1000 * 3600 * 24));

          // Find status elements
          const statusBadge = bookElement.querySelector(".status-badge");
          const statusText = bookElement.querySelector(".status-text");
          const statusBadgeMobile = bookElement.querySelector(
            ".status-badge-mobile"
          );
          const statusTextMobile = bookElement.querySelector(
            ".status-text-mobile"
          );

          let statusClass, statusTextContent, iconClass;

          if (daysDiff < 0) {
            // Overdue
            statusClass = "status-overdue";
            statusTextContent = "Overdue";
            iconClass = "fas fa-exclamation-triangle";
            overdueCount++;
          } else if (daysDiff <= 3) {
            // Due soon
            statusClass = "status-due-soon";
            statusTextContent = "Due Soon";
            iconClass = "fas fa-clock";
            onTimeCount++;
          } else {
            // On time
            statusClass = "status-ok";
            statusTextContent = "On Time";
            iconClass = "fas fa-check-circle";
            onTimeCount++;
          }

          // Update desktop status
          if (statusBadge && statusText) {
            statusBadge.className = `status-badge px-3 py-1 rounded-full text-white text-sm font-medium ${statusClass}`;
            statusText.textContent = statusTextContent;
            const icon = statusBadge.querySelector("i");
            if (icon) {
              icon.className = `${iconClass} text-xs mr-1`;
            }
          }

          // Update mobile status
          if (statusBadgeMobile && statusTextMobile) {
            statusBadgeMobile.className = `status-badge-mobile px-3 py-1 rounded-full text-white text-xs font-medium ${statusClass}`;
            statusTextMobile.textContent = statusTextContent;
            const iconMobile = statusBadgeMobile.querySelector("i");
            if (iconMobile) {
              iconMobile.className = `${iconClass} text-xs mr-1`;
            }
          }
        });

        // Update statistics
        const onTimeElement = document.getElementById("onTimeCount");
        const overdueElement = document.getElementById("overdueCount");
        const totalPenaltyElement = document.getElementById("totalPenalty");

        // if (onTimeElement) onTimeElement.textContent = onTimeCount;
        if (overdueElement) overdueElement.textContent = overdueCount;
        if (totalPenaltyElement)
          totalPenaltyElement.textContent = `${totalPenalty.toFixed(2)}`;
      }

      // Run status update when page loads
      document.addEventListener("DOMContentLoaded", updateBookStatuses);

      // Update statuses every minute
      setInterval(updateBookStatuses, 600);
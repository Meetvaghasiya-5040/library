// Mobile menu toggle
        document.getElementById('mobileMenuButton').addEventListener('click', function() {
            const mobileMenu = document.getElementById('mobileMenu');
            mobileMenu.classList.toggle('hidden');
        });

        // User dropdown toggle
        const userMenuButton = document.getElementById('userMenuButton');
        const userDropdown = document.getElementById('userDropdown');
        
        if (userMenuButton && userDropdown) {
            userMenuButton.addEventListener('click', function() {
                userDropdown.classList.toggle('hidden');
            });
            
            // Close dropdown when clicking outside
            document.addEventListener('click', function(event) {
                if (!userMenuButton.contains(event.target) && !userDropdown.contains(event.target)) {
                    userDropdown.classList.add('hidden');
                }
            });
        }

        // Modal handlers
        const loginBtn = document.getElementById('loginBtn');
        const registerBtn = document.getElementById('registerBtn');
        const loginModal = document.getElementById('loginModal');
        const registerModal = document.getElementById('registerModal');
        
        // Show modals
        if (loginBtn) {
            loginBtn.addEventListener('click', () => {
                loginModal.classList.remove('hidden');
                document.body.style.overflow = 'hidden';
            });
        }
        
        if (registerBtn) {
            registerBtn.addEventListener('click', () => {
                registerModal.classList.remove('hidden');
                document.body.style.overflow = 'hidden';
            });
        }
        
        // Borrow book buttons for non-authenticated users
        const borrowButtons = document.querySelectorAll('[id^="borrowBtn-"]');
        borrowButtons.forEach(button => {
            button.addEventListener('click', () => {
                loginModal.classList.remove('hidden');
                document.body.style.overflow = 'hidden';
            });
        });
        
        // Close modals
        document.getElementById('closeLoginModal').addEventListener('click', () => {
            loginModal.classList.add('hidden');
            document.body.style.overflow = 'auto';
        });
        
        document.getElementById('closeRegisterModal').addEventListener('click', () => {
            registerModal.classList.add('hidden');
            document.body.style.overflow = 'auto';
        });
        
        // Close modals when clicking outside
        [loginModal, registerModal].forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.classList.add('hidden');
                    document.body.style.overflow = 'auto';
                }
            });
        });

        // Message box auto-hide
        const messageBox = document.getElementById('message-box');
        const closeMessage = document.getElementById('closeMessage');
        
        if (messageBox) {
            // Auto hide after 5 seconds
            setTimeout(() => {
                messageBox.style.animation = 'fadeOut 1s ease-out forwards';
                setTimeout(() => messageBox.remove(), 1000);
            }, 5000);
            
            // Manual close
            if (closeMessage) {
                closeMessage.addEventListener('click', () => {
                    messageBox.style.animation = 'fadeOut 0.3s ease-out forwards';
                    setTimeout(() => messageBox.remove(), 300);
                });
            }
        }

        // Real-time search functionality
        const searchInput = document.querySelector('input[name="book_name"]');
        const bookCards = document.querySelectorAll('.book-card');
        const booksGrid = document.querySelector('.grid');
        const emptyState = document.getElementById('no-results-state');
        
        if (searchInput && bookCards.length > 0) {
            // Create no results state if it doesn't exist
            if (!emptyState) {
                const noResultsDiv = document.createElement('div');
                noResultsDiv.id = 'no-results-state';
                noResultsDiv.className = 'hidden text-center py-16 col-span-full';
                noResultsDiv.innerHTML = `
                    <div class="glass-morphism rounded-2xl p-12 max-w-md mx-auto">
                        <div class="bg-gradient-to-r from-orange-500 to-red-600 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6">
                            <i class="fas fa-search text-white text-3xl"></i>
                        </div>
                        <h3 class="text-2xl font-bold text-gray-800 mb-4">No Books Found</h3>
                        <p class="text-gray-600 mb-6">Try adjusting your search terms or browse all books.</p>
                        <button onclick="clearSearch()" class="bg-gradient-to-r from-indigo-500 to-purple-600 text-white px-6 py-3 rounded-lg font-semibold hover:from-indigo-600 hover:to-purple-700 transition-all duration-200 hover-scale inline-flex items-center space-x-2">
                            <i class="fas fa-times"></i>
                            <span>Clear Search</span>
                        </button>
                    </div>
                `;
                if (booksGrid) {
                    booksGrid.appendChild(noResultsDiv);
                }
            }

            // Real-time search filter
            searchInput.addEventListener('input', function() {
                const searchTerm = this.value.toLowerCase().trim();
                let visibleCount = 0;

                bookCards.forEach(card => {
                    const bookTitle = card.querySelector('h3').textContent.toLowerCase();
                    const bookAuthor = card.querySelector('.fa-user').nextElementSibling.textContent.toLowerCase();
                    const bookISBN = card.querySelector('.fa-barcode').nextElementSibling.textContent.toLowerCase();

                    const isMatch = bookTitle.includes(searchTerm) || 
                                   bookAuthor.includes(searchTerm) || 
                                   bookISBN.includes(searchTerm);

                    if (isMatch || searchTerm === '') {
                        card.style.display = 'block';
                        card.style.animation = 'fadeIn 0.3s ease-in-out';
                        visibleCount++;
                    } else {
                        card.style.display = 'none';
                    }
                });

                // Show/hide no results state
                const noResultsState = document.getElementById('no-results-state');
                if (noResultsState) {
                    if (visibleCount === 0 && searchTerm !== '') {
                        noResultsState.classList.remove('hidden');
                        noResultsState.style.animation = 'fadeIn 0.3s ease-in-out';
                    } else {
                        noResultsState.classList.add('hidden');
                    }
                }

                // Update search button text
                const searchButton = document.querySelector('button[type="submit"]');
                if (searchButton) {
                    const buttonText = searchButton.querySelector('span');
                    if (searchTerm.trim()) {
                        buttonText.textContent = `Search (${visibleCount})`;
                        searchButton.classList.add('animate-pulse');
                    } else {
                        buttonText.textContent = 'Search';
                        searchButton.classList.remove('animate-pulse');
                    }
                }
            });

            // Enhanced form submission
            searchInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    // Optional: still submit form for server-side search
                    // this.closest('form').submit();
                }
            });

            // Clear search functionality
            searchInput.addEventListener('focus', function() {
                if (this.value.trim() === '') {
                    // Reset all cards to visible when focusing empty search
                    bookCards.forEach(card => {
                        card.style.display = 'block';
                    });
                    const noResultsState = document.getElementById('no-results-state');
                    if (noResultsState) {
                        noResultsState.classList.add('hidden');
                    }
                }
            });
        }

        // Global clear search function
        window.clearSearch = function() {
            const searchInput = document.querySelector('input[name="book_name"]');
            if (searchInput) {
                searchInput.value = '';
                searchInput.dispatchEvent(new Event('input'));
                searchInput.focus();
            }
        }

        // Add search suggestions (optional enhancement)
        if (searchInput) {
            let searchTimeout;
            searchInput.addEventListener('input', function() {
                clearTimeout(searchTimeout);
                const input = this;
                
                // Add loading state
                searchTimeout = setTimeout(() => {
                    const searchIcon = document.querySelector('.fa-search');
                    if (input.value.trim()) {
                        searchIcon.classList.add('animate-spin');
                        setTimeout(() => {
                            searchIcon.classList.remove('animate-spin');
                        }, 300);
                    }
                }, 100);
            });
        }
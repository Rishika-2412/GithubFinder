class UI {
  constructor() {
    this.profile = document.getElementById("profile");
  }

  showProfile(user) {
    this.profile.innerHTML = `
      <div class="card mb-3 shadow-sm">
        <div class="row g-0">
          <div class="col-md-3 text-center p-3">
            <img src="${user.avatar_url}" class="img-fluid rounded-circle" alt="Avatar" />
            <a href="${user.html_url}" target="_blank" class="btn btn-primary btn-sm mt-2 w-100">View Profile</a>
          </div>
          <div class="col-md-9 p-3">
            <div>
              <span class="badge bg-primary">Public Repos: ${user.public_repos}</span>
              <span class="badge bg-secondary">Public Gists: ${user.public_gists}</span>
              <span class="badge bg-success">Followers: ${user.followers}</span>
              <span class="badge bg-info text-dark">Following: ${user.following}</span>
            </div>
            <ul class="list-group mt-3">
              <li class="list-group-item">Company: ${user.company || "N/A"}</li>
              <li class="list-group-item">Blog: ${user.blog || "N/A"}</li>
              <li class="list-group-item">Location: ${user.location || "N/A"}</li>
              <li class="list-group-item">Member Since: ${new Date(user.created_at).toLocaleDateString()}</li>
            </ul>
          </div>
        </div>
      </div>
      <h4>Latest Repositories</h4>
      <div id="repos" class="mt-3"></div>
    `;
  }

  showRepos(repos, page = 1) {
    let output = "";

    repos.forEach(repo => {
      output += `
        <div class="card card-body mb-2 shadow-sm">
          <div class="d-flex justify-content-between align-items-center">
            <a href="${repo.html_url}" target="_blank"><strong>${repo.name}</strong></a>
            <div>
              <span class="badge bg-primary">⭐ ${repo.stargazers_count}</span>
              <span class="badge bg-secondary">👀 ${repo.watchers_count}</span>
              <span class="badge bg-success">🍴 ${repo.forks_count}</span>
              <span class="badge bg-warning text-dark">${repo.language || "Unknown"}</span>
            </div>
          </div>
        </div>
      `;
    });

    output += `
      <div class="d-flex justify-content-between mt-3">
        <button class="btn btn-outline-secondary" id="prevPage">Previous</button>
        <button class="btn btn-outline-primary" id="nextPage">Next</button>
      </div>
    `;

    document.getElementById("repos").innerHTML = output;

    document.getElementById("prevPage").addEventListener("click", () => {
      if (currentPage > 1) fetchAndRenderUser(currentUser, currentPage - 1);
    });

    document.getElementById("nextPage").addEventListener("click", () => {
      fetchAndRenderUser(currentUser, currentPage + 1);
    });
  }

  showAlert(message, className) {
    this.clearAlert();
    const div = document.createElement("div");
    div.className = className + " alert";
    div.appendChild(document.createTextNode(message));
    const container = document.querySelector(".searchContainer");
    const search = document.querySelector(".card");
    container.insertBefore(div, search);
    setTimeout(() => this.clearAlert(), 3000);
  }

  clearAlert() {
    const currentAlert = document.querySelector(".alert");
    if (currentAlert) currentAlert.remove();
  }

  clearProfile() {
    this.profile.innerHTML = "";
  }

  showLoader() {
    this.profile.innerHTML = `
      <div class="d-flex justify-content-center my-4">
        <div class="spinner-border text-primary" role="status"></div>
      </div>
    `;
  }
}

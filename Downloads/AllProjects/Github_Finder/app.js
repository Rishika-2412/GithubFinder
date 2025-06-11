const github = new Github();
const ui = new UI();

let currentUser = "";
let currentPage = 1;

async function fetchAndRenderUser(user, page = 1) {
  ui.showLoader();

  try {
    const data = await github.getUser(user, page);

    if (data.profile.message === "Not Found") {
      ui.showAlert("User not found", "alert alert-danger");
      ui.clearProfile();
    } else {
      ui.showProfile(data.profile);
      ui.showRepos(data.repos, page);
      currentUser = user;
      currentPage = page;
    }
  } catch (err) {
    console.error("Fetch failed:", err);
    ui.showAlert("Something went wrong", "alert alert-danger");
    ui.clearProfile();
  }
}

document.getElementById("searchBtn").addEventListener("click", () => {
  const userText = document.getElementById("searchUser").value.trim();
  if (userText !== "") fetchAndRenderUser(userText, 1);
  else ui.showAlert("Please enter a username", "alert alert-warning");
});

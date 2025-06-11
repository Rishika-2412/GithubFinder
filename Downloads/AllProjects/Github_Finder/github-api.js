class Github {
  constructor() {
    this.repos_count = 5;
    this.repos_sort = "created: asc";
  }

  async getUser(user, page = 1) {
    try {
      const [profileRes, reposRes] = await Promise.all([
        fetch(`https://api.github.com/users/${user}`),
        fetch(`https://api.github.com/users/${user}/repos?per_page=${this.repos_count}&sort=${this.repos_sort}&page=${page}`)
      ]);

      if (!profileRes.ok || !reposRes.ok) throw new Error("GitHub API error");

      const profile = await profileRes.json();
      const repos = await reposRes.json();

      return { profile, repos };
    } catch (err) {
      console.error("Fetch error:", err);
      return { profile: { message: "Not Found" }, repos: [] };
    }
  }
}

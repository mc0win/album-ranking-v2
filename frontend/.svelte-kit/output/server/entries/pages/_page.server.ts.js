const actions = {
  default: async ({ request }) => {
    const formData = await request.formData();
    const data = { source: formData.get("source"), url: formData.get("link"), round_number: 1, order_number: Math.floor(Math.random() * 54) + 1 };
    await fetch("http://0.0.0.0:8000/albums/...", {
      method: "POST",
      body: JSON.stringify(data)
    });
  }
};
export {
  actions
};

import React, { useState } from "react";
import { posts } from "../api/service";

const CreatePost = () => {
  const [file, setFile] = useState(null);
  const [caption, setCaption] = useState("");

  const handleSubmit = async () => {
    try {
      await posts.uploadAndCreatePost(file, caption);
      alert("Post uploaded!");
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <h2>Create Post</h2>

      <input type="file" onChange={(e) => setFile(e.target.files[0])} />

      <input
        placeholder="Caption"
        onChange={(e) => setCaption(e.target.value)}
      />

      <button onClick={handleSubmit}>Upload</button>
    </div>
  );
};

export default CreatePost;
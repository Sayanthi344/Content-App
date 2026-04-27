import { getUserInfo } from "@/services/apiBlog";
import BlogContainer from "@/ui_components/BlogContainer";
import Hero from "@/ui_components/Hero";
import Spinner from "@/ui_components/Spinner";
import Modal from "@/ui_components/Modal";
import { useQuery } from "@tanstack/react-query";
import { useParams } from "react-router-dom";
import SignupPage from "./SignupPage";
import { useState } from "react";

const ProfilePage = ({ authUsername }) => {
  const [showModal, setShowModal] = useState(false);

  const toggleModal = () => {
    setShowModal(curr => !curr)
  }

  const { username } = useParams();

  const { isPending, isError, data } = useQuery({
    queryKey: ["users", username],
    queryFn: () => getUserInfo(username),
  });

  // ✅ Fix 1 - changed author_posts to blog_posts
  const blogs = data?.blog_posts;

  if (isPending) return <Spinner />;

  // ✅ Fix 2 - added error handling
  if (isError) return <p className="text-center mt-10">Failed to load profile.</p>;

  return (
    <>
      <Hero userInfo={data} authUsername={authUsername} toggleModal={toggleModal} />
      <BlogContainer blogs={blogs} title={`🍔 ${username}'s Posts`} />

      {showModal && (
        <Modal toggleModal={toggleModal}>
          <SignupPage userInfo={data} updateForm={true} toggleModal={toggleModal} />
        </Modal>
      )}
    </>
  );
};

export default ProfilePage;
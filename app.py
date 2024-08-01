require("dotenv").config();
const {
  BlobServiceClient,
  StorageSharedKeyCredential,
} = require("@azure/storage-blob");
const { EmailClient } = require("@azure/communication-email");
const express = require("express");
const bodyParser = require("body-parser");
const app = express();

// This code retrieves your connection string from an environment variable.
console.log(process.env);
const connectionString = process.env.EMAIL_URL;
const client = new EmailClient(connectionString);
// Enter your storage account name and shared key
const account = process.env.STORAGE_ACCOUNT_NAME;
const accountKey = process.env.STORAGE_ACCOUNT_KEY;

// Use StorageSharedKeyCredential with storage account and account key
// StorageSharedKeyCredential is only available in Node.js runtime, not in browsers
const sharedKeyCredential = new StorageSharedKeyCredential(account, accountKey);
const blobServiceClient = new BlobServiceClient(
  `https://${account}.blob.core.windows.net`,
  sharedKeyCredential
);

const containerName = "lab9";
const port = process.env.PORT || 8888;

// middleware
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

async function sendEmail(address, count) {
  const emailMessage = {
    senderAddress:
      "DoNotReply@d0b7c877-a2d0-4b93-bde3-0e75d84c2ab5.azurecomm.net",
    content: {
      subject: "Blob Notification",
      plainText: `There is an change in the blob count ${count}`,
    },
    recipients: {
      to: [{ address: address }],
    },
  };

  const poller = await client.beginSend(emailMessage);
  const result = await poller.pollUntilDone();
  console.log("Result", result);
}

// first fetch all the data from the blob storage
// check how many elements are there
// store that data

let initialCount = 0;
let currentCount = 0;

async function fetchBlobs() {
  console.log("Function is called");
  const containerClient = blobServiceClient.getContainerClient(containerName);

  // need something to store the data
  let tempData = [];

  let blobs = containerClient.listBlobsFlat();
  for await (const blob of blobs) {
    ``;
    tempData.push(blob.name);
    console.log(`Blob: ${blob}`);
    // send mail to the user
    // sendEmail("jaidevv999@gmail.com");
  }

  return tempData;
}

fetchBlobs().then((data) => {
  initialCount = data.length;
});

app.get("/", async (req, res) => {
  let result = await fetchBlobs();

  res.json({ result });
});

setInterval(() => {
  fetchBlobs().then((data) => {
    currentCount = data.length;
    if (currentCount === initialCount) {
      // do nothing
      console.log("There is no change in the count");
    } else {
      console.log("We have to send the notification");
      sendEmail("jaidevv999@gmail.com", currentCount);
      initialCount = currentCount;
    }
  });
}, 2000);

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});

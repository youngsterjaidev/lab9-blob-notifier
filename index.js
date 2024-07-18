const { BlobServiceClient, StorageSharedKeyCredential } = require("@azure/storage-blob");
const { EmailClient } = require("@azure/communication-email");

// This code retrieves your connection string from an environment variable.
const connectionString = "endpoint=";
const client = new EmailClient(connectionString);
// Enter your storage account name and shared key
const account = "";
const accountKey = "";

// Use StorageSharedKeyCredential with storage account and account key
// StorageSharedKeyCredential is only available in Node.js runtime, not in browsers
const sharedKeyCredential = new StorageSharedKeyCredential(account, accountKey);
const blobServiceClient = new BlobServiceClient(
  `https://${account}.blob.core.windows.net`,
  sharedKeyCredential
);

const containerName = "lab9";

async function sendEmail(address) {
    const emailMessage = {
        senderAddress: "DoNotReply@d0b7c877-a2d0-4b93-bde3-0e75d84c2ab5.azurecomm.net",
        content: {
            subject: "For Testing lab9 demo",
            plainText: "Hello world via email.",
        },
        recipients: {
            to: [{ address: address }],
        },
    };

    const poller = await client.beginSend(emailMessage);
    const result = await poller.pollUntilDone();
    console.log("Result", result)
}

async function main() {
    console.log("Function is called")
  const containerClient = blobServiceClient.getContainerClient(containerName);

  let i = 1;
  let blobs = containerClient.listBlobsFlat();
  for await (const blob of blobs) {``
    console.log(`Blob ${i++}: ${blob.name}`);

    // send mail to the user
    sendEmail("jaidevv999@gmail.com")
  }
}



main();
import { Builder, By, until } from 'selenium-webdriver'
import path from 'path';
import fs from 'fs';

export class GetDataMainPageService {
  async execute(): Promise<void> {
    const url = 'https://www.epicgames.com/store/en-US/'
    let driver = await new Builder().forBrowser('chrome').build();

    try {
      await driver.get(url);
      // await driver.wait(until.elementLocated(By.xpath('/html/body/div[1]/div/div[4]/main/div/div[1]/div/nav/div/div[1]/ul/li[2]/a'))).click();

      const element = await driver.wait(until.elementLocated(By.xpath('/html/body/div[1]/div/div[4]/main/div/div[3]/div/div/span[9]/div/div[2]/section/div/div[2]/div/div/div/div/a/div/div/div[3]/div/div/span/div/span'))).getText()

      console.log(element)
   
    } finally {
      await driver.quit();
    }
  }
}